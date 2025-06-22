import os
from ..repository import repo_find
from ..index import index_read, index_write

def cmd_rm(args):
    """
    Handle `minigit rm <paths>…`
    """
    repo = repo_find()
    rm(repo, args.path)

def rm(repo, paths, delete=True, skip_missing=False):
    idx = index_read(repo)
    worktree = repo.worktree + os.sep
    abspaths = {os.path.abspath(p) for p in paths if os.path.abspath(p).startswith(worktree)}
    kept = []
    removed = []
    for e in idx.entries:
        full = os.path.join(repo.worktree, e.name)
        if full in abspaths:
            removed.append(full)
            abspaths.remove(full)
            if delete:
                os.remove(full)
        else:
            kept.append(e)
    if abspaths and not skip_missing:
        raise Exception(f"Paths not in the index: {abspaths}")
    idx.entries = kept
    index_write(repo, idx)
    print(f"Removed {len(removed)} file(s) from the index.")
