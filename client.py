#/usr/bin/env python
import requests
import time
import hashlib
import hmac
import json
import random
path_and_query = "/scheduler/jobs?TIMESTAMP="+str(int(time.time()))+"&ACCOUNT_ID=admin"
source = "http://10.62.2.153/hdmi"
# can ommit file_name_prefix if you dont want one
# allowed chars for filename are:  a-zA-Z0-9_-
metadata = {"name": "channel one euro", "file_name_prefix":"channel1_euro"}
recording_timeout = 10
job_id = "{:x}".format(random.getrandbits(128))

#interval 
seconds = 20
post_body = json.dumps({"name":"human readable job name","func":"jobs:record","args":[source,metadata,recording_timeout],"id":job_id,"trigger": "interval","seconds": seconds})
#cron (command doc: http://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html) 
minute="*/1"
post_body = json.dumps({"name":"human readable job name","func":"jobs:record","args":[source,metadata,recording_timeout],"id":job_id,"trigger": "cron","minute": minute})
#now 
post_body = json.dumps({"name":"human readable job name","func":"jobs:record","args":[source,metadata,recording_timeout],"id":job_id})

#can find command documentation here: 

host = "http://127.0.0.1:5000"
secret = ';hi^897t7utf'.encode()
sig=hmac.new(secret, digestmod=hashlib.sha1, msg=(path_and_query+post_body).encode()).hexdigest()
req = requests.post(host+path_and_query, headers={'X-Auth-Signature': sig},data=post_body)
if req.status_code == 200:
	print(json.dumps(req.json(),indent=4))
