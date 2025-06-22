from ..repository import repo_find
from ..ignore import gitignore_read, check_ignore

def cmd_check_ignore(args):
    """
    Handle `minigit check-ignore <paths>…`
    """
    repo = repo_find()
    rules = gitignore_read(repo)
    for p in args.path:
        if check_ignore(rules, p):
            print(p)
