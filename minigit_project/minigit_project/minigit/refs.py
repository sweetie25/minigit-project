import os

from .repository import repo_file, repo_dir

def ref_resolve(repo, ref):
    path = repo_file(repo, ref)
    if not os.path.isfile(path):
        return None
    data = open(path).read().strip()
    if data.startswith("ref: "):
        # recurse through symbolic ref
        return ref_resolve(repo, data[5:])
    return data

def ref_list(repo, path=None):
    if path is None:
        path = repo_dir(repo, "refs")
    refs = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            refs[name] = ref_list(repo, full)
        else:
            # relpath inside .minigit
            rel = os.path.relpath(full, repo.gitdir)
            refs[name] = ref_resolve(repo, rel)
    return refs

def show_ref(repo, refs, prefix="refs", with_hash=True):
    for name, val in refs.items():
        if isinstance(val, dict):
            show_ref(repo, val, prefix=os.path.join(prefix, name), with_hash=with_hash)
        else:
            if with_hash:
                print(f"{val} {os.path.join(prefix, name)}")
            else:
                print(os.path.join(prefix, name))

def ref_create(repo, ref_name, sha):
    path = repo_file(repo, "refs", ref_name, mkdir=True)
    with open(path, "w") as f:
        f.write(sha + "\n")
