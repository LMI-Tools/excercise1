# Cool Assignment
### usage: commmits_report.py -g \<githubAPIurl\> -r \<repoName\> -u \<repo owner\>  -b \<branch name\> -o \<outputfile\> [-t \<access token\>] | [env variable GITHUB_TOKEN=\<access token\>]

### pytest -q test_commmits_report.py  ( set env varible GITHUB_TOKEN=\<access token\> before executing the test)

### Example:
### python commmits_report.py -g https://api.github.com -r node-demo-app -u rharidoss -b patch-1  -o  /Users/rharidoss/PycharmProjects/excercise1/commit_info.html
