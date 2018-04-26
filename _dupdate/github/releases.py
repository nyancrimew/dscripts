import json
import requests
from collections import namedtuple

def _json_object_hook(d): return namedtuple('Release', d.keys())(*d.values())

def getRelease(user:str, repo:str, version:str):
    r = requests.get(f'https://api.github.com/repos/{user}/{repo}/releases/{version}')
    return r.json(object_hook=_json_object_hook)