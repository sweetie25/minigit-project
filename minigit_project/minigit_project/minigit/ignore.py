import os
from fnmatch import fnmatch

from .repository import repo_file
from .index import index_read
from .objects.base import object_read

def gitignore_parse1(raw):
    raw = raw.strip()
    if not raw or raw.startswith("#"):
        return None
    if raw.startswith("!"):
        return (raw[1:], False)
    if raw.startswith("\\"):
        return (raw[1:], True)
    return (raw, True)

def gitignore_parse(lines):
    rules = []
    for line in lines:
        parsed = gitignore_parse1(line)
        if parsed:
            rules.append(parsed)
    return rules

class GitIgnore:
    def __init__(self):
        self.absolute = []   # list of rule‐lists
        self.scoped = {}     # dir → rule‐list

def gitignore_read(repo):
    ig = GitIgnore()
    # repo/.minigit/info/exclude
    excl = os.path.join(repo.gitdir, "info", "exclude")
    if os.path.exists(excl):
        with open(excl, "r") as f:
            ig.absolute.append(gitignore_parse(f.readlines()))
    # global: XDG_CONFIG_HOME/git/ignore or ~/.config/git/ignore
    cfg = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    global_file = os.path.join(cfg, "git", "ignore")
    if os.path.exists(global_file):
        with open(global_file, "r") as f:
            ig.absolute.append(gitignore_parse(f.readlines()))
    # per-directory .gitignore tracked in index
    idx = index_read(repo)
    for entry in idx.entries:
        if entry.name.endswith(".gitignore"):
            blob = object_read(repo, entry.sha)
            lines = blob.blobdata.decode("utf-8").splitlines()
            dirpath = os.path.dirname(entry.name)
            ig.scoped[dirpath] = gitignore_parse(lines)
    return ig

def check_ignore_scoped(rules_map, path):
    parent = os.path.dirname(path)
    while True:
        if parent in rules_map:
            res = check_ignore1(rules_map[parent], path)
            if res is not None:
                return res
        if parent == "":
            break
        parent = os.path.dirname(parent)
    return None

def check_ignore_absolute(rule_sets, path):
    for rules in rule_sets:
        res = check_ignore1(rules, path)
        if res is not None:
            return res
    return False

def check_ignore(rules, path):
    if os.path.isabs(path):
        raise ValueError("Path must be relative to the repo root")
    scoped = check_ignore_scoped(rules.scoped, path)
    if scoped is not None:
        return scoped
    return check_ignore_absolute(rules.absolute, path)

def check_ignore1(rules, path):
    hit = None
    for pattern, keep in rules:
        if fnmatch(path, pattern):
            hit = keep
    return hit
