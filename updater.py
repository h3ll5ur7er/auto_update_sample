from importlib import reload
from requests import get
from code import interact
import config
from json import dump, loads
from git import get_main_branch, get_file
from dataclasses import asdict

def compare_semver(first: str, second: str) -> int:
    """
        compare two semver strings

        # Example
        >>> compare_semver("1.2.3", "1.2.4")
        -1
        >>> compare_semver("1.2.4", "1.2.4")
        0
        >>> compare_semver("1.2.5", "1.2.4")
        1
        >>> compare_semver("2.0.1", "1.2.4")
        1

    """
    first_parts = [int(part) for part in first.split('.')]
    second_parts = [int(part) for part in second.split('.')]
    for i in range(3):
        if first_parts[i] > second_parts[i]:
            return 1
        if first_parts[i] < second_parts[i]:
            return -1
    return 0

def update(repo: str):
    main_branch = get_main_branch(repo)
    versions_on_main = loads(get_file(repo, "versions.json", main_branch.commit_hash))

    app_version_on_main = versions_on_main.get('semver', None)
    interact(local=locals())
    if app_version_on_main is None:
        print(f"Repo {repo} does not have a semver in versions.json")
        return
    if compare_semver(config.versions.semver, app_version_on_main) >= 0:
        print(f"Repo {repo} is already up to date")
        return
    
    print(f"Repo {repo} is out of date, updating to {app_version_on_main}")

    business_logic_file_content = get_file(repo, "business_logic.py", main_branch.commit_hash)

    for line in business_logic_file_content.splitlines():
        if line.startswith("__version__"):
            remote_app_version = line.partition("=")[2].strip().strip('"')
            break
    with open("business_logic.py") as file:
        local_app_version = [line.partition("=")[2].strip().strip('"') for line in file.read().splitlines() if line.startswith("__version__")][0]
    if compare_semver(local_app_version, remote_app_version) < 0:
        print(f"Updating business_logic.py from {local_app_version} to {remote_app_version}")
        with open("business_logic.py", "w") as file:
            file.write(business_logic_file_content)
    with open("versions.json", "w") as file:
        dump(versions_on_main, file)

def update_all():
    repos = config.Repos()
    for repo in list(asdict(repos)):
        update(repo)

if __name__ == '__main__':
    update_all()
