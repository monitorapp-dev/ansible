#!/bin/env python
#-*- coding: utf-8 -*-

from ansible.module_utils.basic import *
import requests
import json

def Login(sID, sPassword):
    sURL = 'https://localhost:223/v1/auth/login'
    jsQuery = {"id": sID, "pwd": sPassword}
    jsheaders = {"Content-Type": "application/json"}

    response = requests.post(sURL, data=json.dumps(jsQuery), headers=jsheaders, verify=False)
    #response.encoding = 'utf-8'
    
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
   