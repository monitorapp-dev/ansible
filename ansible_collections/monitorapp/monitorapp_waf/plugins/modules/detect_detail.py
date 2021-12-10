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
module: detect_detail
short_description: Detailed view of detected log
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
        description: AIWAF UI super administrator ID.
        type: str
        required: true
    log_id:
        description: Detect log ID
        type: int
        required: true
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Get detect log detail
    detect_detail:
      login_id: "{{ web.id }}"
      login_pwd: "{{ web.password }}"
      log_id: "{{ detect_detail.id }}"
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
client:
  description: Client information
  returned: always
  type: dict
  sample:
    {
      "ip": "10.0.0.67",
      "port": "80"
    }
server:
  description: Client information
  returned: always
  type: dict
  sample:
    {
      "ip": "10.0.0.123",
      "port": "80"
    }
http_version:
  description: Client information
  returned: always
  type: str
  sample: "1.1"
request:
  description: Client information
  returned: always
  type: dict
  sample:
    {
      "data": "R0VUIC9GX0NMX1NlcnZlci9TY2hlZHVsZUxpc3QuYXNwP3N0clN0YXJ0RGF0ZT0yMDE5LTA3LTA
               xJnN0ckVuZERhdGU9MjAxOS0wNy0zMSBIVFRQLzEuMQ0KVXNlci1BZ2VudDogQ29vbGVuZGFyKD
               EuMCkNCkFjY2VwdDogKi8qDQpIb3N0OiAxMC4wLjEuNA0KQ29ubmVjdGlvbjogS2VlcC1BbGl2ZQ0KDQo=",
      "len": 173
    }
domain:
  description: Client information
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
url:
  description: URL
  returned: always
  type: str
  sample: "www.testurl.com"
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
        log_id=dict(type='int', required=True)
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    is_login, token = login(module.params['login_id'], module.params['login_pwd'])

    if is_login is False:
        module.fail_json(msg="Login failed.", meta=token)

    url = 'https://localhost:223/v1/log/detect/' + module.params['log_id']

    headers = {"Content-Type": "application/json", "X-ACCESS-TOKEN": token}
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        module.exit_json(msg="Get successful")
    else:
        module.fail_json(msg="Get failed")

    logout(token)


if __name__ == '__main__':
    main()
