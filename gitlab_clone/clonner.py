import requests
import subprocess, shlex
import argparse
import os
import logging
import urllib3

urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description='Required args for recursive clone')
    parser.add_argument('--group_id', metavar='group_id', type=int,
                        help='Id of a group in gitlab', required=True)

    parser.add_argument('--branch', metavar='branch', type=str,
                        help='Branch to clone in all repos [by default master]', default='master')

    parser.add_argument('--http', help='Clone via http instead of ssh', action='store_true')

    parser.add_argument(
        '--gitlab-url',
        metavar='gitlab',
        type=str,
        default=os.environ.get('GITLAB_URL', "gitlab.com"),
        help='Gitlab address [by default gitlab.com]')

    parser.add_argument(
        '--token',
        metavar='token',
        type=str,
        default=os.environ.get('GITLAB_TOKEN'),
        help='Gitlab Token')

    args = parser.parse_args()
    request_param = args.__dict__

    clone(**request_param)


def clone(group_id, branch, token, gitlab_url, http):
    total_pages = 1
    page = 0
    while page < total_pages:
        page += 1
        response = requests.get(
            f"{gitlab_url}/api/v4/groups/{group_id}/projects?private_token={token}&include_subgroups=True&per_page=100&page={page}&with_shared=False", verify=False)
        for project in response.json():
            path = project['path_with_namespace']
            if http:
                url_to_repo = project[f'http_url_to_repo'].replace("//",f"//token:{token}@")
            else:
                url_to_repo = project[f'ssh_url_to_repo']
            try:
                if not os.path.exists(path):
                    c=f"git clone --branch {branch} {url_to_repo} {path}"
                    logging.info(f"command: {c}")
                    command = shlex.split(c)
                    result_code = subprocess.Popen(command)
                else:
                    logging.info(f"{path} already exists")
                    command = shlex.split(f"cd {path}; git pull  {path}; cd -")
                    result_code = subprocess.Popen(command)

            except Exception as e:
                logging.error(f"Error on {ssh_url_to_repo}: {e}")

        total_pages = int(response.headers['X-Total-Pages'])


if __name__ == '__main__':
    main()
