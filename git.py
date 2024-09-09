""" some acbstractions to work with git """

from dataclasses import dataclass
from requests import get
from typing import Callable, Optional
from base64 import b64decode

@dataclass
class Branch:
    """ branch data """
    name: str
    commit_hash: str
    commit_url: str
    protected: bool

def get_branches(repo: str, condition: Optional[Callable[[Branch], bool]] = None) -> list[Branch]:
    """ get branches for a repo """
    if condition is None:
        condition = lambda branch: True
    branches = [
        Branch(
            name=branch['name'],
            commit_hash=branch['commit']["sha"],
            commit_url=branch['commit']["url"],
            protected=branch['protected']
        )
        for branch in get(f'https://api.github.com/repos/{repo}/branches').json()]
    return [branch for branch in branches if condition(branch)]

def get_main_branch(repo: str) -> Branch:
    """ get the main branch for a repo """
    branches = get_branches(repo, lambda branch: branch.name in ['main', 'master'])
    if len(branches) == 0:
        raise FileNotFoundError(f"Repo {repo} does not have a main branch")
    return branches[0]

def get_file(repo: str, file_path: str, hash: str) -> dict:
    """ get a file from a repo """
    file_metadata = get(f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={hash}").json()
    file_content = file_metadata.get('content', None)
    if file_content is None:
        FileNotFoundError(f"Repo '{repo}' does not have a '{file_path}' file")
        return
    return b64decode(file_content)
