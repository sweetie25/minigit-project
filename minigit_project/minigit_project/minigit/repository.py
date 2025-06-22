import os
import configparser


def repo_path(repo, *paths):
    return os.path.join(repo.gitdir, *paths)


def repo_dir(repo, *paths, mkdir=False):
    full = repo_path(repo, *paths)
    if os.path.exists(full):
        if os.path.isdir(full):
            return full
        raise Exception(f"Not a directory: {full}")
    if mkdir:
        os.makedirs(full)
        return full
    return None


def repo_file(repo, *paths, mkdir=False):
    dirpath = repo_dir(repo, *paths[:-1], mkdir=mkdir)
    if dirpath:
        return repo_path(repo, *paths)


def repo_default_config():
    cfg = configparser.ConfigParser()
    cfg.add_section("core")
    cfg.set("core", "repositoryformatversion", "0")
    cfg.set("core", "filemode", "false")
    cfg.set("core", "bare", "false")
    return cfg

class GitRepository:
    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir   = os.path.join(path, ".minigit")
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a MiniGit repository: {path}")
        self.conf = configparser.ConfigParser()
        cfgfile = repo_file(self, "config")
        if cfgfile and os.path.exists(cfgfile):
            self.conf.read([cfgfile])
        elif not force:
            raise Exception("Configuration file missing.")
        if not force:
            version = int(self.conf.get("core", "repositoryformatversion"))
            if version != 0:
                raise Exception(f"Unsupported repositoryformatversion: {version}")


def repo_create(path):
    """
    Initialize a new repository at the given path.
    """
    repo = GitRepository(path, force=True)
    # ensure worktree exists
    if not os.path.exists(repo.worktree):
        os.makedirs(repo.worktree)

    # create .minigit structure unconditionally
    repo_dir(repo, "branches", mkdir=True)
    repo_dir(repo, "objects", mkdir=True)
    repo_dir(repo, "refs", "tags", mkdir=True)
    repo_dir(repo, "refs", "heads", mkdir=True)

    # description
    with open(repo_file(repo, "description"), "w") as f:
        f.write(
            "Unnamed repository; edit this file 'description' to name the repository.\n"
        )
    # HEAD
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/main\n")
    # config
    with open(repo_file(repo, "config"), "w") as f:
        cfg = repo_default_config()
        cfg.write(f)

    return repo


def repo_find(path=".", required=True):
    path = os.path.realpath(path)
    if os.path.isdir(os.path.join(path, ".minigit")):
        return GitRepository(path)
    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:
        if required:
            raise Exception("Not inside a MiniGit repository.")
        return None
    return repo_find(parent, required=required)
