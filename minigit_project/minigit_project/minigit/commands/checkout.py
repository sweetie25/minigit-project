import os
from ..repository import repo_find, repo_file
from ..objects.base import object_find, object_read


def cmd_checkout(args):
    """
    Handle `minigit checkout <branch|sha>`
    """
    repo = repo_find()
    target = args.target
    branch_path = repo_file(repo, "refs/heads", target)

    # Update HEAD to point to branch or SHA
    if os.path.exists(branch_path):
        with open(branch_path) as f:
            sha = f.read().strip()
        with open(repo_file(repo, "HEAD"), "w") as f:
            f.write(f"ref: refs/heads/{target}\n")
    else:
        sha = object_find(repo, target)
        with open(repo_file(repo, "HEAD"), "w") as f:
            f.write(sha + "\n")

    # Ensure it's a commit
    obj = object_read(repo, sha)
    if obj.fmt != b"commit":
        raise Exception("Can only checkout commits.")
    tree_sha = obj.kvlm[b"tree"].decode()

    # Wipe working tree, skipping .minigit directory entirely
    for root, dirs, files in os.walk(repo.worktree, topdown=False):
        # Skip any path under the .minigit folder
        if root == repo.gitdir or root.startswith(repo.gitdir + os.sep):
            continue
        # Remove files
        for name in files:
            os.remove(os.path.join(root, name))
        # Remove empty directories
        for d in dirs:
            path = os.path.join(root, d)
            if path == repo.gitdir or path.startswith(repo.gitdir + os.sep):
                continue
            try:
                os.rmdir(path)
            except OSError:
                # Directory not empty or in use; ignore
                pass

    # Recreate files from the target tree
    _checkout_tree(repo, object_read(repo, tree_sha), repo.worktree)
    print(f"Checked out to {target}")


def _checkout_tree(repo, tree, path):
    for leaf in tree.items:
        obj = object_read(repo, leaf.sha)
        dest = os.path.join(path, leaf.path)
        if leaf.mode.startswith(b"04"):  # tree => directory
            os.makedirs(dest, exist_ok=True)
            _checkout_tree(repo, obj, dest)
        else:  # blob => file
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(obj.blobdata)
