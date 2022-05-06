import logging
from jinja2 import Template
import argparse
from github import Github
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logging.debug("Start")


# collect data for the report from the API returned JSON response
# returns list  of dictionaries
def getReportData(git_response):
    report_data = []
    for item in git_response:
        report_data.append({'committer': item.commit.committer.name, 'commitID': item.sha, 'msg': item.commit.message})
    return report_data


# generate report using the data
def genReport(repo, branch, commitcount, data, templatepath, outputpath):
    with open(templatepath) as tfile:
        template = Template(tfile.read())
    out = template.render(commits=data, count=commitcount, repo=repo, branch=branch)
    with open(outputpath, "w") as fhtml:
        fhtml.write(out)
    logging.debug('%s  ' % (out))


def validateInputs(input):
    try:
        gh = Github(base_url=input.g, login_or_token=input.t, per_page=5)
        repo = gh.get_repo(f"{input.u}/{input.r}")
        branch = repo.get_branch(branch=input.b)
    except BaseException as e:
        print(str(e))
        exit(-1)
    else:
        return gh.get_repo(f"{input.u}/{input.r}").get_commits(sha=f"{input.b}").get_page(0)


# get user inputs
def getInputs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', required=True)  # git api base url
    parser.add_argument('-r', required=True)  # git repo name
    parser.add_argument('-u', required=True)  # repo owner
    parser.add_argument('-b', required=True)  # branch
    parser.add_argument('-o', required=True)  # output file name
    if 'GITHUB_TOKEN' in os.environ:
        token = {'default': os.environ['GITHUB_TOKEN']}
    else:
        token = {'required': True}
    parser.add_argument('-t', **token)  # specify github access token. overrides GITHUB_TOKEN variable
    return parser.parse_args()


# Script entry
def main():
    args = getInputs()  # collect inputs
    response = validateInputs(args)
    reportdata = getReportData(response)  # Collect the data required for reporting
    maxcommits = 5
    outputfile = args.o
    templatefile = "report_template.html"  # location of the jinja2 report template
    logging.debug('%s  ' % (reportdata))
    genReport(args.r, args.b, maxcommits, reportdata, templatefile, outputfile)  # Create the report using the template


if __name__ == '__main__':
    main()
