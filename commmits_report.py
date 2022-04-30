import json
import logging
from urllib.request import urlopen , HTTPError
from jinja2 import Template
logging .basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug ("Start")

def getCommitData(giturl):
    try:
        response = urlopen(giturl)
    except HTTPError as http_err:
        print(f"HTTP Error : {http_err}")
        exit(0)
    except Exception as err:
        print(f"Error : {err}")
        exit(0)
    else :
        source = response.read()
        return json.loads(source)

def getCommitInfo(data,commit_count) :
    commit_info_list = []
    count = 1
    if (isinstance(data, list)):
        for item in data :
           commit_info_list.append ({'committer': item['commit']['committer']['name'], 'commitID': item['sha'], 'msg': item['commit']['message']})
           count += 1
           if count > commit_count :
               break
    else :
        commit_info_list.append({'committer': data['commit']['committer']['name'], 'commitID': data['sha'],'msg': data['commit']['message']})
    return commit_info_list

def genReport (commitcount,data,path):
    with open(templatepath) as tfile:
        template = Template(tfile.read())

    out = template.render(commits=reportdata,count=commitcount)
    with open(path, "w") as fhtml:
        fhtml.write(out)
    logging.debug('%s  ' % (out))

templatepath = "/Users/rharidoss/git-space/myproject/myproject/report_template.html"
maxcommits=7
data = getCommitData("https://api.github.com/repos/rharidoss/node-demo-app/commits")
reportdata = getCommitInfo(data,maxcommits)
logging.debug('%s  ' % (reportdata))
genReport(maxcommits,reportdata,"/Users/rharidoss/git-space/myproject/myproject/commit_info.html")
