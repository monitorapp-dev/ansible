#!/bin/env python
#-*- coding: utf-8 -*-

from ansible.module_utils.basic import *
import requests
import json
import urllib
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

def detect(sToken, sFrom, sTo, nLimit, nOffset, 
            nDomainID = -1, sClientIP = '', sServerIP = '', nPolicyType = -1):
    sURL = 'https://localhost:223/v1/log/detect'
    
    # Required
    jsQuery = {"from_time": sFrom, "to_time": sTo, "limit": nLimit, "offset": nOffset}

    # Option
    if nDomainID != -1: jsQuery["domain_id"] = nDomainID
    if sClientIP != '': jsQuery["client_ip"] = sClientIP
    if sServerIP != '': jsQuery["server_ip"] = sServerIP
    if nPolicyType != -1: jsQuery["policy_type"] = nPolicyType

    
    jsHeaders = {"Content-Type": "application/json", "X-ACCESS-TOKEN": sToken}
    
    response = requests.get(sURL + '/?' + urllib.urlencode(jsQuery), headers=jsHeaders, verify=False)
     
    if response.text == '':
        return {"response": {}}
    else:
        return {"response": response.json()}

if __name__ == '__main__':
    module_args = dict(
        db_id=dict(type='str', required=True),
        db_password=dict(type='str', required=True),
        from_time=dict(type='str', required=True),
        to_time=dict(type='str', required=True),
        limit=dict(type='int', required=True),
        offset=dict(type='int', required=True),
        domain_id=dict(type='int', required=True),
        client_ip=dict(type='str', required=True),
        server_ip=dict(type='str', required=True),
        policy_type=dict(type='int', required=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    
    jsResult = detect(GetToken(module.params['db_id'], module.params['db_password']),
                        module.params['from_time'], module.params['to_time'], module.params['limit'], module.params['offset'], 
                        module.params['domain_id'], module.params['client_ip'], module.params['server_ip'], module.params['policy_type'])

    if 'error' in jsResult["response"]:
        jsResult["status"] = -1
        module.fail_json(msg=jsResult)
    else:
        jsResult["status"] = 0
        module.exit_json(msg=jsResult)
   