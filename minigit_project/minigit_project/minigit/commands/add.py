import os
from ..repository import repo_find
from ..index import index_read, index_write, GitIndexEntry
from ..objects.base import object_hash
from .rm import rm

def cmd_add(args):
    """
    Handle `minigit add <paths>…`
    """
    repo = repo_find()
    add(repo, args.path)

def add(repo, paths, delete=True, skip_missing=False):
    # first remove any stale entries
    rm(repo, paths, delete=False, skip_missing=True)

    worktree = repo.worktree + os.sep
    to_add = {
        (os.path.abspath(p), os.path.relpath(os.path.abspath(p), repo.worktree))
        for p in paths
        if os.path.isfile(p) and os.path.abspath(p).startswith(worktree)
    }

    idx = index_read(repo)
    for abspath, relpath in to_add:
        with open(abspath, "rb") as f:
            sha = object_hash(f, b"blob", repo)
        st = os.stat(abspath)
        entry = GitIndexEntry(
            ctime=(int(st.st_ctime), st.st_ctime_ns % 10**9),
            mtime=(int(st.st_mtime), st.st_mtime_ns % 10**9),
            dev=st.st_dev,
            ino=st.st_ino,
            mode_type=0b1000,
            mode_perms=0o644,
            uid=st.st_uid,
            gid=st.st_gid,
            fsize=st.st_size,
            sha=sha,
            flag_assume_valid=False,
            flag_stage=0,
            name=relpath
        )
        idx.entries.append(entry)

    index_write(repo, idx)
    print(f"Added {len(to_add)} file(s) to the index.")
