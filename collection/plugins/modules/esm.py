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

def esm(sToken, sEnable, nTransCycle, arServers, arLogTypes, sDelimiter):
    sURL = 'https://localhost:223/v1/config/esm'
    
    jsQuery = {"enable": sEnable, "trans_cycle": nTransCycle, "servers": arServers, "log_types": arLogTypes, "delimiter": sDelimiter}
    
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
        enable=dict(type='str', required=True),
        trans_cycle=dict(type='int', required=True),
        servers=dict(type='list', required=True),
        log_types=dict(type='list', required=True),
        delimiter=dict(type='str', required=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    
    jsResult = esm(GetToken(module.params['db_id'], module.params['db_password']),
                    module.params['enable'], module.params['trans_cycle'], module.params['servers'], module.params['log_types'], module.params['delimiter'])

    if 'error' in jsResult["response"]:
        jsResult["status"] = -1
        module.fail_json(msg=jsResult)
    else:
        jsResult["status"] = 0
        module.exit_json(msg=jsResult)
   