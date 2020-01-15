import requests
import subprocess, shlex
import argparse


def main():
    parser = argparse.ArgumentParser(description='Required args for recursive clone')
    parser.add_argument('--group_id', metavar='group_id', type=int,
                        help='Id of a group in gitlab', required=True)
    parser.add_argument('--token', metavar='token', type=str,
                        help='Gitlab Token', required=True)

    parser.add_argument('--branch', metavar='branch', type=str,
                        help='Branch to clone in all repos [by default master]', default='master')

    parser.add_argument('--gitlab-url', metavar='gitlab', type=str,
                        help='Gitlab address [by default gitlab.com]', default='gitlab.com')
    args = parser.parse_args()
    request_param = args.__dict__

    clone(**request_param)


def clone(group_id, branch, token, gitlab_url):
    total_pages = 1
    page = 0
    while page < total_pages:
        page += 1
        response = requests.get(
            f"https://{gitlab_url}/api/v4/groups/{group_id}/projects?private_token={token}&include_subgroups=True&per_page=100&page={page}&with_shared=False")
        for project in response.json():
            path = project['path_with_namespace']
            ssh_url_to_repo = project['ssh_url_to_repo']

            try:

                command = shlex.split(f"git clone --branch {branch} {ssh_url_to_repo} {path}")
                result_code = subprocess.Popen(command)

            except Exception as e:
                print(f"Error on {ssh_url_to_repo}: {e}")

        total_pages = int(response.headers['X-Total-Pages'])


if __name__ == '__main__':
    main()
