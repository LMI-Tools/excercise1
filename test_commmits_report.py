import argparse
from unittest.mock import patch
import os
import pytest
import commmits_report


def test_inputs():
    args = argparse.Namespace()
    args.g = 'https://api.github.com'
    args.r = 'node-demo-app'
    args.u = 'rharidoss'
    args.b = 'patch-1'
    args.o = '/Users/rharidoss/PycharmProjects/excercise1/commit_info.html'
    args.t = os.environ['GITHUB_TOKEN']
    with patch('commmits_report.getInputs') as mock_inputs:
        mock_inputs.return_value = args
        result = commmits_report.validateInputs(args)
        assert result != None
    mock_inputs.assert_called


@pytest.mark.parametrize('apiurl, repo, owner, branch, outputfile', [(
        'https://api.github.com', 'node-demo-app', 'rharidoss', 'patch-1',
        '/Users/rharidoss/PycharmProjects/excercise1/commit_info_1.html'),
    ('https://api.github.com', 'myproject', 'LMI-Tools', 'patch-1', 'commit_info_2.html'),
    ('https://api.github.com', 'docker-maven-plugin', 'fabric8io', 'integration', 'commit_info_3.html')])
def test_main(apiurl, repo, owner, branch, outputfile):
    args = argparse.Namespace()
    args.g = apiurl
    args.r = repo
    args.u = owner
    args.b = branch
    args.o = outputfile
    args.t = os.getenv('GITHUB_TOKEN', 'none')
    with patch('commmits_report.getInputs') as mock_getInputs:
        mock_getInputs.return_value = args
        commmits_report.main()
