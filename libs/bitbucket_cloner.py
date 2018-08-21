import logging

import requests

from libs.base_cloner import BaseCloner

logger = logging.getLogger(__name__)


class BitbucketCloner(BaseCloner):
    def start(self):
        url = "https://api.bitbucket.org/2.0/repositories/{user}".format(user=self._user)
        r = requests.get(url=url, auth=(self._user, self._token))
        repositories = r.json()["values"]
        for repository in repositories:
            if repository.get("type") != "repository":
                continue

            project_name = repository.get("project").get("name") if "project" in repository else self._user
            repo_name = repository.get("slug")
            repo_url = repository.get("links").get("clone")[0].get("href")
            repo_url = repo_url.replace("@", ":{token}@".format(token=self._token))
            repo_path = self._path.joinpath(self._path, project_name, repo_name)

            if not repo_path.exists():
                logger.debug("Cloning {}".format(repo_name))
                self._clone(repo_url, repo_path)
            else:
                logger.debug("Pulling {}".format(repo_name))
                self._pull(repo_url, repo_path)
