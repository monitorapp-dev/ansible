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
module: blacklist_enable
short_description: Chanege whether to use rule.
description:
    - This module changes whether or not to use IP blacklist rules for AIWAF.
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
    rule_id:
        description: Rule ID
        type: int
        required: true
    enable:
        description: Enables/disables the rule.
        type: int
        required: true
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Enable IP Blacklist
    blacklist_enable:
      login_id: "{{ web.id }}"
      login_pwd: "{{ web.password }}"
      rule_id: "{{ blacklist_enable.id }}"
      enable: "{{ blacklist_enable.enable }}"
    register: result
  - debug: var=result
'''

RETURN = '''
msg:
  description: Success message
  returned: always
  type: str
  sample: 'Update successful'
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
        rule_id=dict(type='int', required=True),
        enable=dict(type='int', required=True)
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    is_login, token = login(module.params['login_id'], module.params['login_pwd'])

    if is_login is False:
        module.fail_json(msg="Login failed.", meta=token)

    url = 'https://localhost:223/v1/policy/admin/ip/blacklist/enable'
    query = {"id": module.params['rule_id'], "enable": module.params['enable']}
    headers = {"Content-Type": "application/json", "X-ACCESS-TOKEN": token}

    response = requests.put(url, data=json.dumps(query), headers=headers, verify=False)

    logout(token)
    if response.status_code == 204:
        module.exit_json(msg="Update successful")
    if response.status_code == 400:
        module.exit_json(msg="Update failed", meta=response.json())
    else:
        module.fail_json(msg="Update failed")


if __name__ == '__main__':
    main()
