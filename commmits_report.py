import logging
from jinja2 import Template
import argparse
from github import Github, GithubException, BadCredentialsException, UnknownObjectException
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logging.debug('Start')


# collect data for the report from the commit data returned by get_commits call
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
    with open(outputpath, 'w') as fhtml:
        fhtml.write(out)
    logging.debug('%s  ' % (out))


# validate the input and get commit data from GitHub
def validateInputs(input, commitcount=5):
    try:
        gh = Github(base_url=input.g, login_or_token=input.t, per_page=commitcount)
        # check if the repo exists
        repo = gh.get_repo(f'{input.u}/{input.r}')
        logging.debug('%s ' % (f'Repo Name: {repo.full_name}'))
        # check if the branch exist
        branch = repo.get_branch(branch=input.b)
        logging.debug('%s ' % (f'Branch Name: {branch.name}'))
        # check if the file directory exist
        if not os.path.isdir(os.path.dirname(input.o) or '.'):
            raise ValueError("Output directory does not exist")
    except ValueError as e:
        print(str(e))
        exit(5)
    except BadCredentialsException:
        print('Bad access token credentials')
        exit(4)
    except UnknownObjectException:
        print('Incorrect owner or repository name')
        exit(3)
    except GithubException:
        print('Branch not found')
        exit(2)
    except FileNotFoundError:
        print('output file path does not exist')
        exit(1)

    else:
        return gh.get_repo(f'{repo.full_name}').get_commits(sha=f'{branch.name}').get_page(0)


# get user inputs
def getInputs():
    parser = argparse.ArgumentParser(
        usage='%(prog)s -g <githubAPIurl> -r <repoName> -u <repo owner>  -b <branch name>, -o <outputfile> [-t <access token>] [env variable GITHUB_TOKEN]')
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
    logging.debug('%s ' % (parser.parse_args()))
    return parser.parse_args()


# Script entry
def main():
    maxcommits = 5
    args = getInputs()  # collect inputs
    response = validateInputs(args, maxcommits)  # validate the input and get commit data from GitHub
    reportdata = getReportData(response)  # Collect the data required for reporting
    outputfile = args.o
    templatefile = 'report_template.html'  # location of the jinja2 report template
    logging.debug('%s  ' % (reportdata))
    genReport(args.r, args.b, maxcommits, reportdata, templatefile, outputfile)  # Create the report using the template
    print('Report successfully generated')


if __name__ == '__main__':
    main()
