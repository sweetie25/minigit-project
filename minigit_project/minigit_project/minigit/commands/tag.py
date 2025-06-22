import os
import configparser
from ..repository import repo_find
from ..refs import ref_list, show_ref, ref_create
from ..objects.base import object_find, object_write
from ..objects.tag import GitTag

def cmd_tag(args):
    repo = repo_find()
    if args.name:
        sha = object_find(repo, args.object)
        if args.create_tag_object:
            tag = GitTag()
            tag.kvlm = {
                b"object": sha.encode(),
                b"type": b"commit",
                b"tag": args.name.encode(),
                b"tagger": gitconfig_user_get(gitconfig_read()).encode(),
                None: b"Tag created by MiniGit\n"
            }
            tag_sha = object_write(tag, repo)
            ref_create(repo, f"tags/{args.name}", tag_sha)
            print(f"Annotated tag {args.name} -> {tag_sha[:7]}")
        else:
            ref_create(repo, f"tags/{args.name}", sha)
            print(f"Tag {args.name} -> {sha[:7]}")
    else:
        tags = ref_list(repo).get("tags", {})
        show_ref(repo, tags, with_hash=False, prefix="refs/tags")

def gitconfig_read():
    cfg = configparser.ConfigParser()
    home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    cfg.read([os.path.join(home, "git", "config"), os.path.expanduser("~/.gitconfig")])
    return cfg

def gitconfig_user_get(cfg):
    if "user" in cfg and "name" in cfg["user"] and "email" in cfg["user"]:
        return f"{cfg['user']['name']} <{cfg['user']['email']}>"
    return "MiniGit User <user@minigit.com>"
