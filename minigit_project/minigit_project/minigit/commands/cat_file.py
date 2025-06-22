from ..repository import repo_find
from ..objects.base import object_read, object_find

def cmd_cat_file(args):
    """
    Handle `minigit cat-file <type> <object>`
    """
    repo = repo_find()
    sha = object_find(repo, args.object, fmt=args.type.encode(), follow=True)
    obj = object_read(repo, sha)
    import sys
    sys.stdout.buffer.write(obj.serialize())
