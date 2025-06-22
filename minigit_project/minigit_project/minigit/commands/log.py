from ..repository import repo_find
from ..objects.base import object_find, object_read

def cmd_log(args):
    """
    Handle `minigit log [commit]`
    """
    repo = repo_find()
    start = object_find(repo, args.commit)
    print("digraph minigitlog{")
    print("  node[shape=rect]")
    _graph(repo, start, set())
    print("}")

def _graph(repo, sha, seen):
    if sha in seen:
        return
    seen.add(sha)
    commit = object_read(repo, sha)
    msg = commit.kvlm[None].decode().split("\n",1)[0]
    msg = msg.replace("\\","\\\\").replace("\"","\\\"")
    print(f"  c_{sha} [label=\"{sha[:7]}: {msg}\"]")
    parents = commit.kvlm.get(b"parent", [])
    if isinstance(parents, bytes):
        parents = [parents]
    for p in parents:
        p_sha = p.decode()
        print(f"  c_{sha} -> c_{p_sha};")
        _graph(repo, p_sha, seen)
