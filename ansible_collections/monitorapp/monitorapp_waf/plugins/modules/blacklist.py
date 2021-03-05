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
module: blacklist
short_description: Get IP blacklist rule.
description:
    - This module queries all information in the AIWAF IP blacklist.
    - Examples include all parameters and values need to be adjusted to datasources before usage.
version_added: "0.1"
author:
    - "Sungjae jang (@sjjang)"
    - "Gahui Yu (@ghyou)"
options:
    login_id:
        description: AIWAF UI super administrator ID
        type: str
        required: true
    login_pwd:
        description: AIWAF UI super administrator password
        type: str
        required: true
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Get IP blacklist
    blacklist:
      login_id: "{{ web.id }}"
      login_pwd: "{{ web.password }}"
    register: result
  - debug: var=result
'''

RETURN = '''
id:
  description: Identification ID
  returned: always
  type: int
  sample: 38
name:
  description: Rule name
  returned: always
  type: str
  sample: "TEST"
enable:
  description: Wheter to use the rule
  returned: always
  type: int
  sample: 1
detect_behavior:
  description: Information about package requirements.
  returned: success
  type: dict
  contains:
    action:
      description : Action
      returned: always
      type: str
      sample: "detect"
    log:
      description : create to log
      returned: always
      type: int
      sample: 1
    mail:
      description : send to mail
      returned: always
      type: int
      sample: 0
    severity:
      description : Severity
      returned: always
      type: str
      sample: medium
detect_target:
  description: Information about package requirements.
  returned: success
  type: dict
  contains:
    client_ip:
      description: Client IP
      returned: always
      type: list
      sample:
        ["10.1.1.99", "10.0.0.100"]
    server_ip:
      description: Server IP and port
      returned: always
      type: list
      sample:
        ["10.1.1.99:80", "10.2.2.33:80"]
vlan_id:
  description: Vlan ID
  returned: always
  type: int
  sample: 50
explain:
  description: Description of the rule
  returned: always
  type: str
  sample: "this is comment.. blah blah..."
idx:
  description: index
  returned: always
  type: str
  sample: 0
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
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    is_login, token = login(module.params['login_id'], module.params['login_pwd'])

    if is_login is False:
        module.fail_json(msg="Login failed.", meta=token)

    url = 'https://localhost:223/v1/policy/admin/ip/blacklist'
    headers = {"Content-Type": "application/json", "X-ACCESS-TOKEN": token}
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code is 200:
        module.exit_json(msg="Get successful", meta=response.json())
    else:
        module.fail_json(msg="Get failed")

    logout(token)


if __name__ == '__main__':
    main()
