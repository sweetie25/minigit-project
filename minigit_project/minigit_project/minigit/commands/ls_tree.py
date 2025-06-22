from ..repository import repo_find
from ..objects.base import object_find, object_read

def cmd_ls_tree(args):
    """
    Handle `minigit ls-tree [-r] <tree-ish>`
    """
    repo = repo_find()
    sha = object_find(repo, args.tree, fmt=b"tree")
    _ls(repo, sha, args.recursive, "")

def _ls(repo, sha, recurse, prefix):
    tree = object_read(repo, sha)
    for leaf in tree.items:
        typ = "tree" if leaf.mode.startswith(b"04") else "blob"
        path = prefix + leaf.path
        print(f"{leaf.mode.decode()} {typ} {leaf.sha}\t{path}")
        if recurse and typ=="tree":
            _ls(repo, leaf.sha, recurse, path + "/")
