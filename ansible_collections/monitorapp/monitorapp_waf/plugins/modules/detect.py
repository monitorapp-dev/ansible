#!/usr/bin/python
# Copyright 2021 Monitorapp, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: detect
short_description: Detection log view
description:
    - This module queries the detection log in the AIWAF.
    - Examples include all parameters and values need to be adjusted to datasources before usage.
version_added: "0.1"
author:
    - "Sungjae jang (@sjjang)"
    - "Gahui Yu (@ghyou)"
options:
    login_id:
        description: AIWAF UI super administrator ID.
        type: str
        required: true
    login_pwd:
        description: AIWAF UI super administrator password.
        type: str
        required: true
    from_time:
        description: Query start time(Y-m-d H:i)
        type: str
        required: true
    to_time:
        description: Query end time(Y-m-d H:i)
        type: str
        required: true
    limit:
        description: Maximum number of displays
        type: int
        required: true
    offset:
        description: Where to start with the data sorted by the latest time order.
        type: int
        required: false
    domain_id:
        description: Domain ID
        type: int
        required: false
    client_ip:
        description: Client IP
        type: str
        required: false
    server_ip:
        description: Server IP
        type: str
        required: false
    policy_type:
        description: Policy code
        type: int
        required: true
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Get detect log
    detect:
      login_id: "{{ web.id }}"
      login_pwd: "{{ web.password }}"
      from_time: "{{ detect.from_time }}"
      to_time: "{{ detect.to_time }}"
      limit: "{{ detect.limit }}"
      offset: "{{ detect.offset }}"
      domain_id: "{{ detect.domain_id }}"
      client_ip: "{{ detect.client_ip }}"
      server_ip: "{{ detect.server_ip }}"
      policy_type: "{{ detect.policy_type }}"
    register: result
  - debug: var=result
'''

RETURN = '''
id:
  description: Log ID
  returned: always
  type: int
  sample: 1
time:
  description: Create log time
  returned: always
  type: str
  sample: '2019-07-16 15:00:00'
country:
  description: country
  returned: always
  type: dict
  sample:
    {
        "code": "KR",
        "text": "KOREA"
    }
client_ip:
  description: Client IP
  returned: always
  type: str
  sample: 10.1.1.23
server_ip:
  description: Client IP
  returned: always
  type: str
  sample: 10.1.1.67
domain:
  description: Domain infomation
  returned: always
  type: dict
  sample:
    {
      "id": 0,
      "text": "Etc."
    }
policy:
  description: Client IP
  returned: always
  type: dict
  sample:
    {
      "type": 53,
      "text": "Priority policy: URL access rule"
    }
rule:
  description: Rule information
  returned: always
  type: dict
  sample:
    {
      "type": 53,
      "text": "Priority policy: URL access rule"
    }
severity:
  description: Severity
  returned: always
  type: dict
  sample:
    {
      "code": "medium",
      "text": "Medium"
    }
action:
  description: Action
  returned: always
  type: dict
  sample:
    {
      "code": "detect",
      "text": "Detect"
    }
mail:
  description: Mail
  returned: always
  type: dict
  sample:
    {
      "code": "0",
      "text": "Not send"
    }
'''

from ansible.module_utils.basic import AnsibleModule
import requests
import json
import urllib.request
import urllib.parse


def login(sID, sPassword):
    sURL = 'https://localhost:223/v1/auth/login'

    jsQuery = {"id": sID, "pwd": sPassword, "lang": "en"}
    jsheaders = {"Content-Type": "application/json"}
    response = requests.post(sURL, data=json.dumps(jsQuery), headers=jsheaders, verify=False)

    dic = json.loads(response.text)
    if response.status_code != 200:
        return False, dic['error']
    else:
        return True, dic['token']


def logout(token):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-access-token': token
    }
    requests.post("https://localhost:223/auth/logout", headers=headers, verify=False)


def main():
    module_args = dict(
        login_id=dict(type='str', required=True),
        login_pwd=dict(type='str', required=True),
        from_time=dict(type='str', required=True),
        to_time=dict(type='str', required=True),
        limit=dict(type='int', required=True),
        offset=dict(type='int', required=True),
        domain_id=dict(type='int', required=True),
        client_ip=dict(type='str', required=True),
        server_ip=dict(type='str', required=True),
        policy_type=dict(type='int', required=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    is_login, token = login(module.params['login_id'], module.params['login_pwd'])

    if is_login is False:
        module.fail_json(msg="Login failed.", meta=token)

    url = 'https://localhost:223/v1/log/detect'

    query = {"from_time": module.params['from_time'], "to_time": module.params['to_time'], "limit": module.params['limit'], "offset": module.params['offset']}

    if module.params['domain_id'] != -1:
        query["domain_id"] = module.params['domain_id']
    if module.params['client_ip'] != '':
        query["client_ip"] = module.params['client_ip']
    if module.params['server_ip'] != '':
        query["server_ip"] = module.params['server_ip']
    if module.params['policy_type'] != -1:
        query["policy_type"] = module.params['policy_type']

    headers = {"Content-Type": "application/json", "X-ACCESS-TOKEN": token}
    response = requests.get(url + '/?' + urllib.parse.urlencode(query), headers=headers, verify=False)

    if response.status_code is 200:
        module.exit_json(msg="Get successful", meta=response.json())
    elif response.status_code is 400:
        module.fail_json(msg="Get failed", meta=response.json())
    else:
        module.fail_json(msg="Get failed")

    logout(token)


if __name__ == '__main__':
    main()
