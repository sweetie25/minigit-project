import os
from datetime import datetime
import configparser
from ..repository import repo_find, repo_file
from ..index import index_read
from ..objects.base import object_find, object_write
from ..objects.commit import GitCommit
from ..objects.tree import GitTree, GitTreeLeaf
from ..refs import ref_resolve
from .branch import get_active_branch

def cmd_commit(args):
    """
    Handle `minigit commit -m "msg"`
    """
    repo = repo_find()
    idx = index_read(repo)
    tree = _tree_from_index(repo, idx)
    parent = object_find(repo, "HEAD")
    author = _gitconfig_user_get(_gitconfig_read())
    new_sha = _commit_create(repo, tree, [parent] if parent else [], author, datetime.now(), args.message)
    branch = get_active_branch(repo)
    ref = f"refs/heads/{branch}" if branch else "HEAD"
    with open(repo_file(repo, ref), "w") as f:
        f.write(new_sha + "\n")
    print(f"Committed {new_sha[:7]}")

def _tree_from_index(repo, idx):
    """
    Build a tree object from the index entries.
    """
    # simple flat-tree for illustration
    tree = GitTree()
    for e in idx.entries:
        leaf = GitTreeLeaf(mode=b"100644", path=e.name, sha=e.sha)
        tree.items.append(leaf)
    return object_write(tree, repo)

def _commit_create(repo, tree_sha, parents, author, ts, msg):
    c = GitCommit()
    c.kvlm[b"tree"] = tree_sha.encode()
    if parents:
        c.kvlm[b"parent"] = [p.encode() for p in parents] if len(parents) > 1 else parents[0].encode()
    offset = ts.utcoffset().total_seconds() if ts.utcoffset() else 0
    tz = f"{'+' if offset>=0 else '-'}{int(abs(offset)//3600):02d}{int(abs(offset)%3600//60):02d}"
    meta = f"{author} {int(ts.timestamp())} {tz}".encode()
    c.kvlm[b"author"]    = meta
    c.kvlm[b"committer"] = meta
    c.kvlm[None]         = msg.encode()
    return object_write(c, repo)

def _gitconfig_read():
    cfg = configparser.ConfigParser()
    home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    cfg.read([os.path.join(home,"git","config"), os.path.expanduser("~/.gitconfig")])
    return cfg

def _gitconfig_user_get(cfg):
    if "user" in cfg and "name" in cfg["user"] and "email" in cfg["user"]:
        return f"{cfg['user']['name']} <{cfg['user']['email']}>"
    return "MiniGit User <minigit@local>"
