import json
import logging
from urllib.request import urlopen , HTTPError
from jinja2 import Template
import argparse
logging .basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logging.debug ("Start")

# Use Github api to get limited recent commits made in the branch. Returns json object or array of json objects
# TO DO : Cache the API call to provide faster responses
def getGithubData(giturl):
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

# collect data for the report from the API returned JSON response
#returns list  of dictionaries
def getReportData(git_response) :
    report_data = []
    #response data had multiple commits data
    if (isinstance(git_response, list)):
        for item in git_response :
           report_data.append ({'committer': item['commit']['committer']['name'], 'commitID': item['sha'], 'msg': item['commit']['message']})
    else :
        # Response has single commit data
        report_data.append({'committer': data['commit']['committer']['name'], 'commitID': data['sha'],'msg': data['commit']['message']})
    return report_data

# generate report using the data
def genReport (repo,branch,commitcount,data,templatepath,outputpath):
    with open(templatepath) as tfile:
        template = Template(tfile.read())
    out = template.render(commits=data,count=commitcount,repo=repo,branch=branch)
    with open(outputpath, "w") as fhtml:
        fhtml.write(out)
    logging.debug('%s  ' % (out))

#get user inputs
def getInputs() :
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', required=True) # git api base url
    parser.add_argument('-r', required=True) # git repo name
    parser.add_argument('-u', required=True) # repo owner
    parser.add_argument('-b', required=True) # branch
    parser.add_argument('-o', required=True) # output file name
    return parser.parse_args()
# Script entry
def main() :
    args = getInputs()  # collect inputs
    maxcommits = 5
    git_api = f"{args.g}/repos/{args.u}/{args.r}/commits?sha={args.b}&per_page={maxcommits}&page=1"  # construct the github API
    logging.debug('%s  ' % (git_api))
    outputfile = f"{args.o}"    # the report goes here
    templatefile = "report_template.html"  # location of the jinja2 report template
    response = getGithubData(git_api)  # Get commit info from github
    reportdata = getReportData(response)  # Collect the data required for reporting
    logging.debug('%s  ' % (reportdata))
    genReport(args.r,args.b,maxcommits,reportdata,templatefile,outputfile)  # Create the report using the template

if __name__ == '__main__' :
    main()
