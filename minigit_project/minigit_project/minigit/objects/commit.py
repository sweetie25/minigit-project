from .base import GitObject
from ..utils import kvlm_parse, kvlm_serialize

class GitCommit(GitObject):
    fmt = b"commit"

    def deserialize(self, data):
        # parse headers and message
        self.kvlm = kvlm_parse(data)

    def serialize(self):
        return kvlm_serialize(self.kvlm)

    def init(self):
        # empty commit: no headers yet
        self.kvlm = {}
