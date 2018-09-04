import logging

from github import Github

from libs.base_cloner import BaseCloner

logger = logging.getLogger(__name__)


class GithubCloner(BaseCloner):
    def start(self):
        base_url = "github.com"
        handler = Github(login_or_token=self._token)

        for repo in handler.get_user().get_repos():
            repo_name = repo.name

            url = "https://{user}:{token}@{base_url}/{user}/{repo_name}.git".format(user=self._user,
                                                                                    token=self._token,
                                                                                    repo_name=repo_name,
                                                                                    base_url=base_url)

            repo_path = self._path.joinpath(repo_name)

            if not repo_path.exists():
                logger.debug("Cloning {}".format(repo_name))
                self._clone(url, repo_path)
            else:
                logger.debug("Pulling {}".format(repo_name))
                self._pull(url, repo_path)
