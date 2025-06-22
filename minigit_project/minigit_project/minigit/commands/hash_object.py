import sys
from ..repository import repo_find
from ..objects.base import object_hash

def cmd_hash_object(args):
    """
    Handle `minigit hash-object [-w] -t type <path>`
    """
    repo = repo_find() if args.write else None
    with open(args.path,"rb") as f:
        sha = object_hash(f, args.type.encode(), repo)
    print(sha)
