import difflib
from ..repository import repo_find
from ..objects.base import object_read, object_find

def cmd_diff(args):
    repo = repo_find()
    sha1 = object_find(repo, args.commit1)
    sha2 = object_find(repo, args.commit2)
    dict1 = tree_to_dict(repo, sha1)
    dict2 = tree_to_dict(repo, sha2)
    for path in sorted(set(dict1) | set(dict2)):
        b1, b2 = dict1.get(path), dict2.get(path)
        if b1 == b2:
            continue
        if b1 is None:
            print(f"Only in {args.commit2}: {path}")
        elif b2 is None:
            print(f"Only in {args.commit1}: {path}")
        else:
            c1 = object_read(repo, b1).blobdata.decode("utf-8").splitlines()
            c2 = object_read(repo, b2).blobdata.decode("utf-8").splitlines()
            for line in difflib.unified_diff(c1, c2, fromfile=path, tofile=path, lineterm=""):
                print(line)

def tree_to_dict(repo, commit_sha, prefix=""):
    from ..objects.base import object_find, object_read
    # resolve commit → tree SHA
    obj = object_read(repo, object_find(repo, commit_sha, fmt=b"commit"))
    tree_sha = obj.kvlm[b"tree"].decode()
    # now traverse
    def _traverse(tsha, pref):
        d = {}
        tree = object_read(repo, object_find(repo, tsha, fmt=b"tree"))
        for leaf in tree.items:
            p = pref + leaf.path
            if leaf.mode.startswith(b"04"):
                d.update(_traverse(leaf.sha, p + "/"))
            else:
                d[p] = leaf.sha
        return d
    return _traverse(tree_sha, prefix)
