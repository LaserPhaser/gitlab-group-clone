import requests
import multiprocessing
import time
import subprocess, shlex
import argparse
import os
import logging
import urllib3
import threading
from concurrent.futures import ProcessPoolExecutor
            
urllib3.disable_warnings()
class LogPipe(threading.Thread):
                
    def __init__(self, level, tag):
        """Setup the object with a logger and a loglevel
        and start the thread
        """
        threading.Thread.__init__(self)
        self.daemon = False
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.tag = tag
        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe"""
        return self.fdWrite

    def run(self):
        """Run the thread, logging everything."""
        for line in iter(self.pipeReader.readline, ''):
            logging.log(self.level, f"{self.tag} :: {line.strip()}")
        self.pipeReader.close()
        
    def close(self):
        """Close the write end of the pipe."""
        os.close(self.fdWrite)
        
    def write(self):
        """If your code has something like sys.stdout.write"""
        logging.log(self.level, f"{self.tag} :: {line.strip()}")
                
    def flush(self):
        """If you code has something like this sys.stdout.flush"""
        pass    
                    
def main():     
    parser = argparse.ArgumentParser(description='Required args for recursive clone')
    parser.add_argument('--group_id', metavar='group_id', type=int,
                        help='Id of a group in gitlab', required=True)
                    
    parser.add_argument('--branch', metavar='branch', type=str,
                        help='Branch to clone in all repos [by default the projects default_branch]')
                
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
    logging.basicConfig(level="INFO")
    clone(**request_param)
    
def worker(command, c, path=None):
    try:
        if path is None:
            logging.info(f"begin worker {c}")
            lpipe = LogPipe(logging.INFO, c)
            epipe = LogPipe(logging.ERROR, c)
            with subprocess.Popen(command, stdout=lpipe, stderr=epipe) as proc:
                lpipe.close() # prevent deadlocks
                epipe.close() # prevent deadlocks
                logging.info(f"close {c}")
        else:
            logging.info(f"begin worker {path} {c}")
            lpipe = LogPipe(logging.INFO, f"cd {path};{c};cd -")
            epipe = LogPipe(logging.ERROR, f"cd {path};{c};cd -")
            with subprocess.Popen(command, cwd=path, stdout=lpipe, stderr=epipe) as proc:
                lpipe.close() # prevent deadlocks
                epipe.close() # prevent deadlocks
                logging.info(f"close {path} {c}")

    except Exception as e:
        logging.error(f"Error on {url_to_repo}: {e}")


def clone(group_id, branch, token, gitlab_url, http):
    total_pages = 1
    page = 0
    while page < total_pages:
        page += 1
        url = f"{gitlab_url}/api/v4/groups/{group_id}/projects?private_token={token}&include_subgroups=True&per_page=100&page={page}&with_shared=False"
        logging.info(f"url: {url}")
        response = requests.get(url, verify=False)
        current_branch = branch
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as pool:
            for project in response.json():
                path = project['path_with_namespace']
                logging.info(f"for {path}")
                if branch is None:
                    current_branch = project['default_branch']
                    logging.info(f"new branch: {current_branch} {path}")
                if http:
                    url_to_repo = project[f'http_url_to_repo'].replace("//",f"//token:{token}@")
                else:
                    url_to_repo = project[f'ssh_url_to_repo']
                if not os.path.exists(path):
                    c=f"git clone --branch {current_branch} {url_to_repo} {path}"
                    logging.info(f"command: {c}")
                    command = shlex.split(c)
                    pool.submit(worker,command,c)
                else:
                    logging.info(f"{path} already exists")
                    c = "git pull"
                    logging.info(f"command {c}")
                    command = shlex.split(c)
                    pool.submit(worker,command,c,path)
        total_pages = int(response.headers['X-Total-Pages'])

if __name__ == '__main__':
    main()
