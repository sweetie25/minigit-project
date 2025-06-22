import os
import zlib
import hashlib
from ..repository import repo_file

class GitObject:
    fmt = None

    def __init__(self, data=None):
        if data is not None:
            self.deserialize(data)
        else:
            self.init()

    def serialize(self):
        raise NotImplementedError()

    def deserialize(self, data):
        raise NotImplementedError()

    def init(self):
        pass

def object_read(repo, sha):
    """
    Read object by SHA, decompress, parse header, and
    return an instance of the right GitObject subclass.
    """
    path = repo_file(repo, "objects", sha[:2], sha[2:])
    if not os.path.isfile(path):
        return None
    raw = zlib.decompress(open(path, "rb").read())
    # header: "<fmt> <size>\0"
    x = raw.find(b" ")
    fmt = raw[:x]
    y = raw.find(b"\x00", x)
    size = int(raw[x+1:y])
    if size != len(raw) - y - 1:
        raise Exception(f"Malformed object {sha}: bad length")
    data = raw[y+1:]

    # only now import each subclass
    if fmt == b"blob":
        from .blob import GitBlob as _Cls
    elif fmt == b"commit":
        from .commit import GitCommit as _Cls
    elif fmt == b"tree":
        from .tree import GitTree as _Cls
    elif fmt == b"tag":
        from .tag import GitTag as _Cls
    else:
        raise Exception(f"Unknown object type {fmt.decode()} for {sha}")

    return _Cls(data)

def object_write(obj, repo=None):
    """
    Serialize an object, compute its SHA1, and
    optionally write it into the repo’s object database.
    """
    data = obj.serialize()
    header = obj.fmt + b" " + str(len(data)).encode() + b"\x00"
    full = header + data
    sha = hashlib.sha1(full).hexdigest()
    if repo:
        path = repo_file(repo, "objects", sha[:2], sha[2:], mkdir=True)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(zlib.compress(full))
    return sha

def object_hash(fd, fmt, repo=None):
    """
    Read file-like fd, wrap it in the right object,
    and write (if requested) to repo. Returns its sha.
    """
    if fmt == b"blob":
        from .blob import GitBlob as _Cls
    elif fmt == b"commit":
        from .commit import GitCommit as _Cls
    elif fmt == b"tree":
        from .tree import GitTree as _Cls
    elif fmt == b"tag":
        from .tag import GitTag as _Cls
    else:
        raise Exception(f"Unknown type {fmt!r}")
    obj = _Cls(fd.read())
    return object_write(obj, repo)

def object_find(repo, name, fmt=None, follow=True):
    """
    Resolve a name to a SHA. If fmt is given, follow tags/commits
    to find an object of that type.
    """
    from ..refs import ref_resolve

    # HEAD or branches/tags
    if name == "HEAD":
        shas = [ref_resolve(repo, "HEAD")]
    elif len(name) >= 4 and all(c in "0123456789abcdef" for c in name.lower()):
        # abbreviated SHA logic
        prefix, rest = name[:2], name[2:]
        objdir = repo_file(repo, "objects", prefix)
        shas = []
        if os.path.isdir(objdir):
            for fname in os.listdir(objdir):
                if fname.startswith(rest):
                    shas.append(prefix + fname)
    else:
        # branch or tag
        tag_sha = ref_resolve(repo, f"refs/tags/{name}")
        head_sha = ref_resolve(repo, f"refs/heads/{name}")
        shas = [sha for sha in (tag_sha, head_sha) if sha]

    if not shas:
        raise Exception(f"No such reference {name}.")
    if len(shas) > 1:
        raise Exception(f"Ambiguous reference {name}: {shas}")
    sha = shas[0]

    if not fmt:
        return sha

    # peel until matching fmt
    while True:
        obj = object_read(repo, sha)
        if obj.fmt == fmt:
            return sha
        if not follow:
            return None
        if obj.fmt == b"tag":
            sha = obj.kvlm[b"object"].decode()
        elif obj.fmt == b"commit" and fmt == b"tree":
            sha = obj.kvlm[b"tree"].decode()
        else:
            return None
