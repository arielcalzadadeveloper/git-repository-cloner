import json
import logging
import os
import pathlib
import time

from libs.bitbucket_cloner import BitbucketCloner
from libs.exceptions import GitRepositoryClonerException
from libs.github_cloner import GithubCloner


def main():
    base_dir = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

    # Setup logging
    log_path = "{}".format(base_dir.joinpath("logs", "git_repository_cloner.log").absolute())
    log_level = logging.DEBUG
    log_format = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
    logging.basicConfig(filename=log_path, level=log_level, format=log_format)
    logger = logging.getLogger(__name__)

    # Read configuration
    configuration_file_path = base_dir.joinpath("config.json")
    if not configuration_file_path.exists():
        message = "There's not configuration file"
        logger.exception(message)
        raise GitRepositoryClonerException(message)

    with configuration_file_path.open() as json_file:
        configuration = json.load(json_file)

    # Parse configuration
    for credentials in configuration:
        user = credentials.get("user")
        token = credentials.get("token")
        path = credentials.get("path")
        repo_type = credentials.get("type")
        enabled = credentials.get("enabled")

        if not enabled:
            logger.debug("Repos for user {} is disabled, process skipped".format(user))
            continue

        logger.info("Starting to clone or pull repos for user {}".format(user))

        if repo_type == "GITHUB":
            cloner_class = GithubCloner
        elif repo_type == "BITBUCKET":
            cloner_class = BitbucketCloner
        else:
            message = "Cloner class not found"
            logger.exception(message)
            raise GitRepositoryClonerException(message)

        cloner = cloner_class(user, token, path)
        start_time = time.time()
        cloner.start()
        end_time = time.time()
        logging.debug("Process executed in {:.2f}s".format(end_time - start_time))


if __name__ == "__main__":
    main()
