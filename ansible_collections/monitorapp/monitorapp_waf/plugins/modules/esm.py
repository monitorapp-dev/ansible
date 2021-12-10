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
module: esm
short_description: ESM settings.
description:
    - This module settings or change ESM server information and log format to transfer.
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
        description: Enables/disables the ESM.
        type: str
        required: true
    trans_cycle:
        description: Transmission cycle
        type: int
        required: true
    servers:
        description: ESM server address(protocol, ip, port)
        type: list
        required: true
    log_types:
        description: ESM log types
        type: list
        required: true
    delimiter:
        description: Log delimiter
        type: str
        required: true
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Request esm server setting
    esm:
      login_id: "{{ web.id }}"
      login_pwd: "{{ web.password }}"
      enable: "{{ esm.enable }}"
      trans_cycle: "{{ esm.trans_cycle }}"
      servers: "{{ esm.servers }}"
      log_types: "{{ esm.log_types }}"
      delimiter: "{{ esm.delimiter }}"
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


def call(url, token, data):
    headers = {"Content-Type": "application/json", "X-ACCESS-TOKEN": token}
    response = requests.put(url, data=json.dumps(data), headers=headers, verify=False)
    ret = False
    if response.status_code >= 200 and response.status_code < 300:
        ret = True

    return ret, response


def main():
    module_args = dict(
        login_id=dict(type='str', required=True),
        login_pwd=dict(type='str', required=True),
        enable=dict(type='str', required=True),
        trans_cycle=dict(type='int', required=True),
        servers=dict(type='list', required=True),
        log_types=dict(type='list', required=True),
        delimiter=dict(type='str', required=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    is_login, token = login(module.params['login_id'], module.params['login_pwd'])

    if is_login is False:
        module.fail_json(msg="Login failed.", meta=token)

    data = {"enable": module.params['enable'],
            "trans_cycle": module.params['trans_cycle'],
            "servers": module.params['servers'],
            "log_types": module.params['log_types'],
            "delimiter": module.params['delimiter']}

    url = 'https://localhost:223/v1/config/esm'
    result, res = call(url, token, data)
    logout(token)

    if result:
        if res.status_code == 200:
            module.exit_json(msg="Update successful", changed=result, meta=res.json())
        else:
            module.exit_json(msg="Update successful", changed=result)
    else:
        module.fail_json(msg="Update failed", meta=res.json())


if __name__ == '__main__':
    main()
