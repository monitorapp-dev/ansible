#!/bin/env python
#-*- coding: utf-8 -*-

from ansible.module_utils.basic import *
import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor

def GetToken(sDBID, sDBPassword):
    pgCon = psycopg2.connect(dbname='aiwaf_db', user=sDBID, host='localhost', password=sDBPassword)
    pgCur = pgCon.cursor(cursor_factory=psycopg2.extras.DictCursor)
    pgCur.execute("SELECT * FROM api_tokens ORDER BY id DESC LIMIT 1")
    jsResult = pgCur.fetchone()
    if jsResult is not None:
        sToken = jsResult["token"]
    else:
        sToken = ''
    pgCur.close()
    pgCon.close()    

    return sToken

def whitelistEnable(sToken, nID, nEnable):
    sURL = 'https://localhost:223/v1/policy/admin/ip/whitelist/enable'
    
    jsQuery = {"id": nID, "enable": nEnable}
    
    jsHeaders = {"Content-Type": "application/json", "X-ACCESS-TOKEN": sToken}
    
    response = requests.put(sURL, data=json.dumps(jsQuery), headers=jsHeaders, verify=False)
     
    if response.text == '':
        return {"response": {}}
    else:
        return {"response": response.json()}

if __name__ == '__main__':
    module_args = dict(
        db_id=dict(type='str', required=True),
        db_password=dict(type='str', required=True),
        id=dict(type='int', required=True),
        enable=dict(type='int', required=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    jsResult = whitelistEnable(GetToken(module.params['db_id'], module.params['db_password']),
                    module.params['id'], module.params['enable'])

    if 'error' in jsResult["response"]:
        jsResult["status"] = -1
        module.fail_json(msg=jsResult)
    else:
        jsResult["status"] = 0
        module.exit_json(msg=jsResult)
   