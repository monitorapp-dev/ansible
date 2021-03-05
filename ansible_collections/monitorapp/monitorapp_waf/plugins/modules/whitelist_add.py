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
module: whitelist_add
short_description: Add IP whitelist rule.
description:
    - This module queries all information in the AIWAF IP whitelist.
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
    enable:
        description: Enables/disables the rule.
        type: int
        required: true
    name:
        description: Rule name
        type: str
        required: true
    detect_target:
        description: Detect target
        type: dict
        required: true
        suboptions:
            client_ip:
                description: Client IP
                type: list
            server_ip:
                description: Server IP
                type: list
    vlan_id:
        description: Vlan ID
        type: int
        required: true
    explain:
        description: Description of the rule
        type: str
        required: false
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Add IP Whitelist
    whitelist_add:
      login_id: "{{ web.id }}"
      login_pwd: "{{ web.password }}"
      enable: "{{ whitelist_add.enable }}"
      name: "{{ whitelist_add.name }}"
      detect_target: "{{ whitelist_add.detect_target }}"
      vlan_id: "{{ whitelist_add.vlan_id }}"
    explain: "{{ whitelist_add.explain }}"
    register: result
  - debug: var=result
'''

RETURN = '''
id:
  description: Rule ID
  returned: always
  type: int
  sample: 36
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
        enable=dict(type='int', required=True),
        name=dict(type='str', required=True),
        detect_target=dict(type='dict', required=True),
        vlan_id=dict(type='int', required=True),
        explain=dict(type='str', required=True)
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    is_login, token = login(module.params['login_id'], module.params['login_pwd'])

    if is_login is False:
        module.fail_json(msg="Login failed.", meta=token)

    url = 'https://localhost:223/v1/policy/admin/ip/whitelist'
    headers = {"Content-Type": "application/json", "X-ACCESS-TOKEN": token}
    query = {"enable": module.params['enable'], "name": module.params['name'],
             "detect_target": module.params['detect_target'], "vlan_id": module.params['vlan_id'],
             "explain": module.params['explain']}

    response = requests.post(url, data=json.dumps(query), headers=headers, verify=False)

    if response.status_code == 200:
        module.exit_json(msg="Update successful", meta=response.json())
    elif response.status_code == 400:
        module.fail_json(msg="Update failed", meta=response.json())
    else:
        module.fail_json(msg="Update failed")


if __name__ == '__main__':
    main()
