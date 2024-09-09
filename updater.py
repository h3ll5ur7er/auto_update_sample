from importlib import reload
from requests import get
from code import interact
from config import Config
from dataclasses import dataclass
from json import dump

@dataclass
class Branch:
    name: str
    commit_hash: str
    commit_url: str
    protected: bool

def update(repo: str):
    branch_data = get(f'https://api.github.com/repos/{repo}/branches').json()
    branches = [Branch(name=branch['name'], commit_hash=branch['commit']["sha"], commit_url=branch['commit']["url"], protected=branch['protected']) for branch in branch_data]
    main_branches = list(filter(lambda branch: branch.name in ['main', 'master'], branches))
    if len(main_branches) == 0:
        print(f"Repo {repo} does not have a main branch")
        return
    main_branch = main_branches[0]
    versions_on_main = get(f"https://api.github.com/repos/{repo}/contents/versions.json?ref={main_branch.commit_hash}").json()
    app_version_on_main = versions_on_main.get('semver', None)
    if app_version_on_main is None:
        print(f"Repo {repo} does not have a semver in versions.json")
        return
    if config.versions.semver == app_version_on_main:
        print(f"Repo {repo} is already up to date")
        return
    print(f"Repo {repo} is out of date, updating to {app_version_on_main}") #todo
    with open("versions.json", "w") as file:
        dump(versions_on_main, file)
if __name__ == '__main__':
    config = Config()
    update(config.repos.auto_update_sample)

