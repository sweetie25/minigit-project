from .commit import GitCommit

class GitTag(GitCommit):
    fmt = b"tag"
    # inherits deserialize/serialize from GitCommit
