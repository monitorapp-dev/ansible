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
module: apply_admin_policy
short_description: Apply admin policy.
description:
    - This module  provides the ability to apply admin policy of AIWAF.
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
        description: AIWAF UI super administrator ID
        type: str
        required: true
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Apply admin policy
    apply_admin_policy:
      login_id: "{{ web.id }}"
      login_pwd: "{{ web.password }}"
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
        login_pwd=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    is_login, token = login(module.params['login_id'], module.params['login_pwd'])

    if is_login is False:
        module.fail_json(msg="Login failed.", meta=token)

    url = 'https://localhost:223/v1/policy/admin/apply'
    headers = {"Content-Type": "application/json", "X-ACCESS-TOKEN": token}
    response = requests.post(url, data=json.dumps({}), headers=headers, verify=False)

    if response.status_code == 204:
        module.exit_json(msg="Update successful")
    else:
        module.fail_json(msg="Update failed", meta=response.json())

    logout(token)


if __name__ == '__main__':
    main()
