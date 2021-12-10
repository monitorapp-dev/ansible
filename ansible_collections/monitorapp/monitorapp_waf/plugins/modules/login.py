# #-*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
import requests
import json
__metaclass__ = type

DOCUMENTATION = '''
---
module: login
short_description: UI login
description:
    - This module performs login to UI of AIWAF.
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
'''

EXAMPLES = '''
- hosts: all
  remote_user: root
  gather_facts: yes
  tasks:
  - name: Request time sync
    time:
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


def Login(sID, sPassword):
    sURL = 'https://localhost:223/v1/auth/login'
    jsQuery = {"id": sID, "pwd": sPassword}
    jsheaders = {"Content-Type": "application/json"}

    response = requests.post(sURL, data=json.dumps(jsQuery), headers=jsheaders, verify=False)

    return {"response": response.json()}


if __name__ == '__main__':
    module_args = dict(
        id=dict(type='str', required=True),
        password=dict(type='str', required=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    jsResult = Login(module.params['id'], module.params['password'])

    if 'error' in jsResult["response"]:
        jsResult["status"] = -1
        module.fail_json(msg=jsResult)
    else:
        jsResult["status"] = 0
        module.exit_json(msg=jsResult)
