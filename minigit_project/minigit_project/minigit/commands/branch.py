import os
from ..repository import repo_find, repo_file
from ..objects.base import object_find

def get_active_branch(repo):
    head = open(repo_file(repo,"HEAD")).read().strip()
    if head.startswith("ref: refs/heads/"):
        return head[16:]
    return None

def cmd_branch(args):
    """
    Handle `minigit branch <name>`
    """
    repo = repo_find()
    sha = object_find(repo, "HEAD")
    path = repo_file(repo, "refs/heads", args.name, mkdir=True)
    if os.path.exists(path):
        raise Exception(f"Branch {args.name} already exists.")
    with open(path,"w") as f:
        f.write(sha + "\n")
    print(f"Branch {args.name} created at {sha[:7]}")
