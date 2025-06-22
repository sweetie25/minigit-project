from ..repository import repo_find
from ..index import index_read

def cmd_ls_files(args):
    """
    Handle `minigit ls-files [--verbose]`
    """
    repo = repo_find()
    idx = index_read(repo)
    if args.verbose:
        print(f"Index v{idx.version}, {len(idx.entries)} entries")
    for e in idx.entries:
        print(e.name)
        if args.verbose:
            print(f"  SHA: {e.sha}")
