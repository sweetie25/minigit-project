import os
from .base import GitObject, object_read
from ..repository import repo_file

class GitTreeLeaf:
    def __init__(self, mode, path, sha):
        self.mode = mode      # e.g. b"100644" or b"040000"
        self.path = path      # string
        self.sha  = sha       # hex string

def tree_parse_one(raw, start=0):
    """
    Parse a single entry from a raw Git tree.
    Returns (next_pos, GitTreeLeaf).
    """
    spc = raw.find(b" ", start)
    mode = raw[start:spc]
    nul = raw.find(b"\x00", spc)
    path = raw[spc+1:nul].decode("utf-8")
    sha_bytes = raw[nul+1:nul+21]
    sha = sha_bytes.hex()
    return nul + 21, GitTreeLeaf(mode, path, sha)

def tree_parse(raw):
    pos = 0
    items = []
    while pos < len(raw):
        pos, leaf = tree_parse_one(raw, pos)
        items.append(leaf)
    return items

def tree_serialize(tree_obj):
    """
    Given a GitTree (with .items), produce its raw content bytes.
    """
    tree_obj.items.sort(key=lambda it: it.path)
    out = b""
    for leaf in tree_obj.items:
        out += leaf.mode + b" " + leaf.path.encode("utf-8") + b"\x00"
        out += bytes.fromhex(leaf.sha)
    return out

class GitTree(GitObject):
    fmt = b"tree"

    def deserialize(self, data):
        self.items = tree_parse(data)

    def serialize(self):
        return tree_serialize(self)

    def init(self):
        self.items = []

def tree_checkout(repo, tree, dest_path):
    """
    Write a tree object (and subtrees) out into the working directory.
    """
    os.makedirs(dest_path, exist_ok=True)
    for leaf in tree.items:
        obj = object_read(repo, leaf.sha)
        target = os.path.join(dest_path, leaf.path)
        if leaf.mode.startswith(b"04"):  # directory
            tree_checkout(repo, obj, target)
        else:  # blob
            with open(target, "wb") as f:
                f.write(obj.blobdata)
