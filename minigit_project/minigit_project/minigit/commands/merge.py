import os
import configparser
from datetime import datetime
from ..repository import repo_find, repo_file
from ..refs import ref_resolve
from ..objects.base import object_read, object_find, object_write
from ..objects.tree import GitTree, GitTreeLeaf
from .branch import get_active_branch

def cmd_merge(args):
    repo = repo_find()
    current_branch = get_active_branch(repo)
    if not current_branch:
        raise Exception("Cannot merge in detached HEAD state.")
    target_branch = args.branch
    target_commit = ref_resolve(repo, f"refs/heads/{target_branch}")
    if not target_commit:
        raise Exception(f"No such branch: {target_branch}")
    current_commit = ref_resolve(repo, "HEAD")
    ancestor = find_common_ancestor(repo, current_commit, target_commit)
    if not ancestor:
        raise Exception("No common ancestor found.")
    current_tree = get_tree(repo, current_commit)
    target_tree = get_tree(repo, target_commit)
    ancestor_tree = get_tree(repo, ancestor)
    merged_tree = merge_trees(repo, ancestor_tree, current_tree, target_tree)
    author = gitconfig_user_get(gitconfig_read())
    new_sha = commit_create(
        repo, merged_tree,
        [current_commit, target_commit],
        author,
        datetime.now(),
        f"Merge branch '{target_branch}' into '{current_branch}'"
    )
    head_ref = repo_file(repo, "refs", "heads", current_branch)
    with open(head_ref, "w") as f:
        f.write(new_sha + "\n")
    print(f"Merged branch {target_branch} into {current_branch}")

def get_tree(repo, commit_sha):
    c = object_read(repo, commit_sha)
    return c.kvlm[b"tree"].decode()

def get_commit_history(repo, sha):
    seen = set()
    stack = [sha]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        commit = object_read(repo, cur)
        parents = commit.kvlm.get(b"parent", [])
        if isinstance(parents, bytes):
            parents = [parents]
        for p in parents:
            stack.append(p.decode())
    return seen

def find_common_ancestor(repo, c1, c2):
    h1 = get_commit_history(repo, c1)
    h2 = get_commit_history(repo, c2)
    common = h1 & h2
    return next(iter(common), None)

def tree_to_dict(repo, tree_sha, prefix=""):
    from ..objects.base import object_find, object_read
    sha = object_find(repo, tree_sha, fmt=b"tree")
    tree = object_read(repo, sha)
    d = {}
    for leaf in tree.items:
        path = prefix + leaf.path
        if leaf.mode.startswith(b"04"):
            d.update(tree_to_dict(repo, leaf.sha, path + "/"))
        else:
            d[path] = leaf.sha
    return d

def merge_trees(repo, ancestor_sha, current_sha, target_sha):
    a = tree_to_dict(repo, ancestor_sha)
    c = tree_to_dict(repo, current_sha)
    t = tree_to_dict(repo, target_sha)
    merged = {}
    for path in set(a) | set(c) | set(t):
        av, cv, tv = a.get(path), c.get(path), t.get(path)
        if cv == tv:
            merged[path] = cv
        elif cv == av:
            merged[path] = tv
        elif tv == av:
            merged[path] = cv
        else:
            raise Exception(f"CONFLICT: both modified {path}")
    tree = GitTree()
    for p, sha in merged.items():
        tree.items.append(GitTreeLeaf(mode=b"100644", path=p, sha=sha))
    return object_write(tree, repo)

def commit_create(repo, tree_sha, parents, author, ts, msg):
    from ..objects.commit import GitCommit
    c = GitCommit()
    c.kvlm[b"tree"] = tree_sha.encode()
    if parents:
        if len(parents) > 1:
            c.kvlm[b"parent"] = [p.encode() for p in parents]
        else:
            c.kvlm[b"parent"] = parents[0].encode()
    offset = ts.utcoffset().total_seconds() if ts.utcoffset() else 0
    tz = f"{'+' if offset>=0 else '-'}{int(abs(offset)//3600):02d}{int(abs(offset)%3600//60):02d}"
    meta = f"{author} {int(ts.timestamp())} {tz}".encode()
    c.kvlm[b"author"] = meta
    c.kvlm[b"committer"] = meta
    c.kvlm[None] = msg.encode()
    return object_write(c, repo)

def gitconfig_read():
    cfg = configparser.ConfigParser()
    home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    cfg.read([os.path.join(home, "git", "config"), os.path.expanduser("~/.gitconfig")])
    return cfg

def gitconfig_user_get(cfg):
    if "user" in cfg and "name" in cfg["user"] and "email" in cfg["user"]:
        return f"{cfg['user']['name']} <{cfg['user']['email']}>"
    return "MiniGit User <minigit@local>"
