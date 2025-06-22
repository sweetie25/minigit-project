import os
from ..repository import repo_find
from ..index import index_read
from ..refs import ref_resolve
from .branch import get_active_branch


def cmd_status(args):
    """
    Handle `minigit status`.
    Compares HEAD tree vs index entries to show added, modified, deleted.
    """
    repo = repo_find()
    idx = index_read(repo)
    branch = get_active_branch(repo)
    head_ref = ref_resolve(repo, "HEAD")
    if branch:
        print(f"On branch {branch}")
    else:
        print(f"HEAD detached at {head_ref}")

    # Build HEAD tree map: path -> sha
    head_tree = _build_tree_map(repo, head_ref) if head_ref else {}

    # Track files from HEAD not in index
    remaining = dict(head_tree)

    # Compare index vs HEAD
    for entry in idx.entries:
        if entry.name in head_tree:
            if head_tree[entry.name] != entry.sha:
                print(f"  modified: {entry.name}")
            remaining.pop(entry.name, None)
        else:
            print(f"  added:    {entry.name}")

    # Files in HEAD not in index
    for path in sorted(remaining):
        print(f"  deleted:  {path}")


def _build_tree_map(repo, ref, prefix=""):
    """
    Recursively build a map of file paths to blob SHAs from a commit or tree reference.
    """
    from ..objects.base import object_read, object_find

    # Resolve commit -> tree SHA
    try:
        commit_sha = object_find(repo, ref, fmt=b"commit")
        commit = object_read(repo, commit_sha)
        tree_sha = commit.kvlm[b"tree"].decode()
    except Exception:
        # maybe ref is already a tree SHA
        tree_sha = object_find(repo, ref, fmt=b"tree")

    def _recurse(tree_sha, base):
        tree = object_read(repo, object_find(repo, tree_sha, fmt=b"tree"))
        mapping = {}
        for leaf in tree.items:
            path = os.path.join(base, leaf.path)
            if leaf.mode.startswith(b"04"):
                mapping.update(_recurse(leaf.sha, path))
            else:
                mapping[path] = leaf.sha
        return mapping

    return _recurse(tree_sha, prefix)
