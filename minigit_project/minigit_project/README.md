# MiniGit

MiniGit is a lightweight, custom version control system inspired by Git. It provides essential VCS features—repository initialization, staging, committing, branching, merging, diffing, tagging, and status checks—without external dependencies.

---

## Features

- **Init**: Create a new repository (`minigit init`).
- **Add / Remove**: Stage or unstage files (`minigit add`, `minigit rm`).
- **Commit**: Record snapshots of your project (`minigit commit -m "message"`).
- **Log**: View commit history as a Graphviz `digraph` (`minigit log`).
- **Branch & Checkout**: Create and switch branches (`minigit branch`, `minigit checkout`).
- **Merge**: Three-way merge with conflict detection (`minigit merge`).
- **Diff**: Unified diff between any two commits (`minigit diff`).
- **Tag**: Lightweight and annotated tags (`minigit tag`).
- **Status**: Show working tree status vs. index and HEAD (`minigit status`).
- **Ignore**: Support for `.gitignore`-style patterns.

---

## Installation

```bash
cd /path/to/minigit_project
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
pip3 install --upgrade pip
pip3 install -e .                # install MiniGit in editable mode

## Quick Start & Manual Testing

# Follow these steps to verify MiniGit works end-to-end:

# 1. Create a new demo repo
mkdir ~/minigit-demo && cd ~/minigit-demo
minigit init .

# 3. add & commit
echo "hello world" > a.txt

minigit add a.txt
minigit status
# →   added:    a.txt

minigit commit -m "first commit"
# →   Committed <SHA1>

# 4. Inspect history
minigit log

# 5. Branch & checkout
minigit branch feature
# →   Branch feature created at <SHA1>
minigit checkout feature
# →   Checked out to feature

# 6. Make a feature change
echo "feature work" > feat.txt
minigit add feat.txt
minigit commit -m "add feat.txt"
# →   Committed <SHA2>
ls
# →   a.txt  feat.txt

# 7. Switch back & merge
minigit checkout main
# →   Checked out to main
ls
# →   a.txt

minigit merge feature
# →   Merged branch feature into main
ls
# →   a.txt  feat.txt

# 8. Verify history after merge
minigit log


# 9. Tagging
minigit tag v1.0 main
# →   Tag v1.0 -> <SHA>
minigit tag -a v1.1 main
# →   Annotated tag v1.1 -> <SHA>
minigit show-ref
# →   Lists refs/heads/main, refs/heads/feature, refs/tags/v1.0, refs/tags/v1.1


# 11. Final status check
minigit status

## Command Reference
| Command                                  | Description                                    |                              |
| ---------------------------------------- | ---------------------------------------------- | ---------------------------- |
| `minigit init <dir>`                     | Initialize a new repository                    |                              |
| `minigit add <files>`                    | Add files to the staging area (index)          |                              |
| `minigit rm <files>`                     | Remove files from index and working tree       |                              |
| `minigit commit -m "msg"`                | Commit staged changes                          |                              |
| `minigit log [<commit>]`                 | Show commit history as Graphviz digraph        |                              |
| `minigit branch <name>`                  | Create a new branch at HEAD                    |                              |
| \`minigit checkout \<branch              | sha>\`                                         | Switch to a branch or commit |
| `minigit merge <branch>`                 | Merge specified branch into current branch     |                              |
| `minigit diff <sha1> <sha2>`             | Show unified diff between two commits          |                              |
| `minigit tag [-a] [name] [obj]`          | List or create tags (annotated or lightweight) |                              |
| `minigit show-ref`                       | List all references (heads & tags)             |                              |
| `minigit status`                         | Show working tree status vs. index & HEAD      |                              |
| `minigit hash-object ...`                | Compute and optionally store object SHA        |                              |
| `minigit cat-file <type> <obj>`          | Show object contents (blob, commit, tag, tree) |                              |
| `minigit ls-tree [-r] <tree>`            | List tree contents                             |                              |
| `minigit ls-files [--verbose]`           | List entries in the index                      |                              |
| `minigit rev-parse [--wyag-type] <name>` | Resolve refs/abbrev. SHAs                      |                              |
| `minigit check-ignore <paths>`           | Check ignore rules against paths               |                              |
```
