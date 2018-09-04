import logging
import os
import pathlib
import subprocess

from libs.exceptions import GitRepositoryClonerException

logger = logging.getLogger(__name__)


class BaseCloner:
    def __init__(self, user, token, path, base_url=None):
        self._user = user
        self._token = token
        self._path = pathlib.Path(path)
        self._base_url = base_url

        # Create path if not exists
        if not self._path.exists():
            os.makedirs("{}".format(self._path.absolute()))

    def start(self):
        pass

    def _clone(self, url, repo_path):
        command = [
            "git",
            "clone",
            url,
            "{}".format(repo_path.absolute())
        ]
        self._run_command(command)

    def _pull(self, url, repo_path):
        os.chdir("{}".format(repo_path.absolute()))
        command = [
            "git",
            "pull",
            url
        ]
        self._run_command(command)

    @staticmethod
    def _run_command(command):
        logger.debug("Running command: {}".format(command))

        try:
            command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process_output, _ = command_line_process.communicate()

            if command_line_process.returncode != 0:
                logger.exception(process_output)
                raise GitRepositoryClonerException(process_output)
        except Exception as e:
            logger.exception(e)
            raise GitRepositoryClonerException(e)
