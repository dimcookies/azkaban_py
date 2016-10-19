import requests,json
import sys, datetime

AZKABAN_BASE_URL = 'http://AZKABANURL/'
AZKABAN_USERNAME = "USERNAME"
AZKABAN_PASSWORD = "PASSWORD"

AZKABAN_REST_HEADERS = { 'Content-Type' : 'application/x-www-form-urlencoded', 'X-Requested-With' : 'XMLHttpRequest'}
STATE_FILE = "state"

#perform login and return session id to be used in next calls
def login():
    url = AZKABAN_BASE_URL
    data = 'action=login&username=%s&password=%s' % (AZKABAN_USERNAME, AZKABAN_PASSWORD)
    response = requests.post(url, headers=AZKABAN_REST_HEADERS, data=data)
    res = json.loads(response.content)
    if res.has_key('error'):
        raise Exception("Error during login: %s" % res['error'])
    return res['session.id']

#get job id to start from.
#taken from command line argument or state file
def getLastExecution():
    args = sys.argv
    if len(args) > 1:
        start = int(args[1])
    else:
        try:
            start = int(open(STATE_FILE).readline())
        except:
            start = 0
    return start

#retrieve stats for a job
def getJobStats(session_id, id):
    url = AZKABAN_BASE_URL + 'executor'
    data = 'session.id=%s&ajax=fetchexecflow&execid=%s' % (session_id, id)
    response = requests.post(url, headers=AZKABAN_REST_HEADERS, data=data)
    res = json.loads(response.content)
    if res.has_key('error'):
        if res['error'] == "Cannot find execution '%s'" % (id):
            #case of non existing job id
            return None
        else:
            raise Exception("Unknown error for id:%s => %s" %(id, res['error']))
    return res

#converts millis to a date object
def millisToDate(millis):
    return datetime.datetime.fromtimestamp(int(millis)/1000.0)

job_id = getLastExecution()
print "Starting from id:%s" % (job_id)
session_id = login()

while True:
    res = getJobStats(session_id, job_id)
    if not res: #non existing jobs
        break
    job_status = res['status']
    if job_status == 'RUNNING':
        print "Job %s is currently running, stopping iteration" % job_id
        #break if a job is running in order to wait it finish
        break
    if job_status != 'SUCCEEDED':
        print job_id, res['project'], job_status, millisToDate(res['startTime']), millisToDate(res['endTime'])

    job_id +=1

print "Last job id checked: %s" % (job_id-1)
#write state so that next run will continue from there
open(STATE_FILE,"w").write(str(job_id))

