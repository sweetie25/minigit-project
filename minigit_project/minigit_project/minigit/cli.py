import argparse
import sys

from .commands.init import cmd_init
from .commands.add import cmd_add
from .commands.commit import cmd_commit
from .commands.log import cmd_log
from .commands.branch import cmd_branch
from .commands.checkout import cmd_checkout
from .commands.merge import cmd_merge
from .commands.diff import cmd_diff
from .commands.cat_file import cmd_cat_file
from .commands.hash_object import cmd_hash_object
from .commands.ls_tree import cmd_ls_tree
from .commands.show_ref import cmd_show_ref
from .commands.tag import cmd_tag
from .commands.rev_parse import cmd_rev_parse
from .commands.ls_files import cmd_ls_files
from .commands.check_ignore import cmd_check_ignore
from .commands.status import cmd_status
from .commands.rm import cmd_rm

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description="MiniGit: A Custom Version Control System")
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True

    # init
    p = subparsers.add_parser("init", help="Initialize a new, empty repository.")
    p.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repository.")
    p.set_defaults(func=cmd_init)

    # add
    p = subparsers.add_parser("add", help="Add files contents to the index.")
    p.add_argument("path", nargs="+", help="Files to add")
    p.set_defaults(func=cmd_add)

    # commit
    p = subparsers.add_parser("commit", help="Record changes to the repository.")
    p.add_argument("-m", metavar="message", dest="message", help="Message to associate with this commit.")
    p.set_defaults(func=cmd_commit)

    # log
    p = subparsers.add_parser("log", help="Display history of a given commit.")
    p.add_argument("commit", nargs="?", default="HEAD", help="Commit to start at.")
    p.set_defaults(func=cmd_log)

    # branch
    p = subparsers.add_parser("branch", help="Create a new branch.")
    p.add_argument("name", help="Name of the new branch.")
    p.set_defaults(func=cmd_branch)

    # checkout
    p = subparsers.add_parser("checkout", help="Checkout a commit or branch.")
    p.add_argument("target", help="Branch name or commit hash to checkout.")
    p.set_defaults(func=cmd_checkout)

    # merge
    p = subparsers.add_parser("merge", help="Merge a branch into the current branch.")
    p.add_argument("branch", help="Name of the branch to merge.")
    p.set_defaults(func=cmd_merge)

    # diff
    p = subparsers.add_parser("diff", help="Show differences between commits.")
    p.add_argument("commit1", help="First commit.")
    p.add_argument("commit2", help="Second commit.")
    p.set_defaults(func=cmd_diff)

    # cat-file
    p = subparsers.add_parser("cat-file", help="Provide content of repository objects")
    p.add_argument("type", choices=["blob", "commit", "tag", "tree"], help="Specify the type")
    p.add_argument("object", help="The object to display")
    p.set_defaults(func=cmd_cat_file)

    # hash-object
    p = subparsers.add_parser("hash-object", help="Compute object ID and optionally create a blob from a file")
    p.add_argument("-t", metavar="type", dest="type", choices=["blob", "commit", "tag", "tree"], default="blob", help="Specify the type")
    p.add_argument("-w", dest="write", action="store_true", help="Actually write the object into the database")
    p.add_argument("path", help="Read object from <file>")
    p.set_defaults(func=cmd_hash_object)

    # ls-tree
    p = subparsers.add_parser("ls-tree", help="Pretty-print a tree object.")
    p.add_argument("-r", dest="recursive", action="store_true", help="Recurse into sub-trees")
    p.add_argument("tree", help="A tree-ish object.")
    p.set_defaults(func=cmd_ls_tree)

    # show-ref
    p = subparsers.add_parser("show-ref", help="List references.")
    p.set_defaults(func=cmd_show_ref)

    # tag
    p = subparsers.add_parser("tag", help="List and create tags")
    p.add_argument("-a", action="store_true", dest="create_tag_object", help="Whether to create a tag object")
    p.add_argument("name", nargs="?", help="The new tag's name")
    p.add_argument("object", nargs="?", default="HEAD", help="The object the new tag will point to")
    p.set_defaults(func=cmd_tag)

    # rev-parse
    p = subparsers.add_parser("rev-parse", help="Parse revision (or other objects) identifiers")
    p.add_argument("--wyag-type", metavar="type", dest="type", choices=["blob", "commit", "tag", "tree"], default=None, help="Specify the expected type")
    p.add_argument("name", help="The name to parse")
    p.set_defaults(func=cmd_rev_parse)

    # ls-files
    p = subparsers.add_parser("ls-files", help="List all the staged files")
    p.add_argument("--verbose", action="store_true", help="Show detailed index info.")
    p.set_defaults(func=cmd_ls_files)

    # check-ignore
    p = subparsers.add_parser("check-ignore", help="Check path(s) against ignore rules.")
    p.add_argument("path", nargs="+", help="Paths to check")
    p.set_defaults(func=cmd_check_ignore)

    # status
    p = subparsers.add_parser("status", help="Show the working tree status.")
    p.set_defaults(func=cmd_status)

    # rm
    p = subparsers.add_parser("rm", help="Remove files from the working tree and the index.")
    p.add_argument("path", nargs="+", help="Files to remove")
    p.set_defaults(func=cmd_rm)

    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
