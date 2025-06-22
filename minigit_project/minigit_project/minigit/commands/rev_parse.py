from ..repository import repo_find
from ..objects.base import object_find

def cmd_rev_parse(args):
    """
    Handle `minigit rev-parse [--wyag-type type] <name>`
    """
    repo = repo_find()
    sha = object_find(repo, args.name, fmt=(args.type.encode() if args.type else None))
    print(sha)
