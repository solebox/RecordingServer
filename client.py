import requests
import time
import hashlib
import hmac
import json
path_and_query = "/scheduler/jobs?TIMESTAMP="+str(int(time.time()))+"&ACCOUNT_ID=admin"

post_body = json.dumps({"name":"yaron","func":"jobs:record","args":["http://10.62.2.153/hdmi",{"name":"london","file_name_prefix":"yaronz"},10],"id":"job22"})

host = "http://127.0.0.1:5000"
secret = ';hi^897t7utf'.encode()
sig=hmac.new(secret, digestmod=hashlib.sha1, msg=(path_and_query+post_body).encode()).hexdigest()
req = requests.post(host+path_and_query, headers={'X-Auth-Signature': sig},data=post_body)
print(req.content)
print(req.request.body)
