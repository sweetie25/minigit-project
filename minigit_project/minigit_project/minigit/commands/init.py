from ..repository import repo_create

def cmd_init(args):
    """
    Handle `minigit init [path]`
    """
    repo = repo_create(args.path)
    print(f"Initialized empty MiniGit repository in {args.path}/.minigit")
