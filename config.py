""" excel converter config file """
from dataclasses import dataclass
from json import load

__version__ = "0.0.1"

@dataclass
class Versions:
    """ versions """
    semver: str = "0.0.1"
    auto_update_sample: str = "b16bf372032545c27da82da628bce6d75de46071"

@dataclass
class Repos:
    """ versions """
    auto_update_sample: str = "h3ll5ur7er/auto_update_sample"

@dataclass
class Config:
    """ config """
    versions: Versions
    repos: Repos

    def __init__(self):
        with open("versions.json") as file:
            data = load(file)
        self.versions = Versions(**data)
        self.repos = Repos()
    @classmethod
    def from_dict(cls, dikt: dict):
        """Returns the config object from a dictionary"""
        return cls(Versions(**dikt), Repos())