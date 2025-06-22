import os
from math import ceil
from datetime import datetime

from .repository import repo_file

class GitIndexEntry:
    def __init__(self, ctime, mtime, dev, ino, mode_type, mode_perms,
                 uid, gid, fsize, sha, flag_assume_valid, flag_stage, name):
        self.ctime = ctime
        self.mtime = mtime
        self.dev = dev
        self.ino = ino
        self.mode_type = mode_type
        self.mode_perms = mode_perms
        self.uid = uid
        self.gid = gid
        self.fsize = fsize
        self.sha = sha
        self.flag_assume_valid = flag_assume_valid
        self.flag_stage = flag_stage
        self.name = name

class GitIndex:
    def __init__(self, version=2, entries=None):
        self.version = version
        self.entries = entries or []

def index_read(repo):
    index_path = repo_file(repo, "index")
    if not os.path.exists(index_path):
        return GitIndex()
    data = open(index_path, "rb").read()
    # header: "DIRC" | version (4) | count (4)
    assert data[:4] == b"DIRC"
    version = int.from_bytes(data[4:8], "big")
    count   = int.from_bytes(data[8:12], "big")
    entries = []
    idx = 12
    for _ in range(count):
        # read fixed‐size metadata
        ctime_s = int.from_bytes(data[idx:idx+4], "big")
        ctime_ns= int.from_bytes(data[idx+4:idx+8], "big")
        mtime_s = int.from_bytes(data[idx+8:idx+12], "big")
        mtime_ns= int.from_bytes(data[idx+12:idx+16], "big")
        dev     = int.from_bytes(data[idx+16:idx+20], "big")
        ino     = int.from_bytes(data[idx+20:idx+24], "big")
        mode    = int.from_bytes(data[idx+24:idx+28], "big")
        mode_type = mode >> 12
        mode_perms= mode & 0o7777
        uid     = int.from_bytes(data[idx+28:idx+32], "big")
        gid     = int.from_bytes(data[idx+32:idx+36], "big")
        fsize   = int.from_bytes(data[idx+36:idx+40], "big")
        sha     = format(int.from_bytes(data[idx+40:idx+60], "big"), "040x")
        flags   = int.from_bytes(data[idx+60:idx+62], "big")
        flag_assume_valid = bool(flags & 0x8000)
        flag_stage        = (flags >> 12) & 0b11
        name_len = flags & 0x0FFF
        idx += 62
        name = data[idx:idx+name_len].decode("utf-8")
        idx += name_len + 1
        # align to 8-byte boundary
        if idx % 8:
            idx += (8 - (idx % 8))
        entries.append(GitIndexEntry(
            ctime=(ctime_s, ctime_ns),
            mtime=(mtime_s, mtime_ns),
            dev=dev, ino=ino,
            mode_type=mode_type,
            mode_perms=mode_perms,
            uid=uid, gid=gid,
            fsize=fsize,
            sha=sha,
            flag_assume_valid=flag_assume_valid,
            flag_stage=flag_stage,
            name=name
        ))
    return GitIndex(version=version, entries=entries)

def index_write(repo, index):
    out = bytearray()
    out += b"DIRC"
    out += index.version.to_bytes(4, "big")
    out += len(index.entries).to_bytes(4, "big")
    pos = 12
    for e in index.entries:
        out += e.ctime[0].to_bytes(4, "big")
        out += e.ctime[1].to_bytes(4, "big")
        out += e.mtime[0].to_bytes(4, "big")
        out += e.mtime[1].to_bytes(4, "big")
        out += (e.dev & 0xFFFFFFFF).to_bytes(4, "big")
        out += (e.ino & 0xFFFFFFFF).to_bytes(4, "big")
        mode = (e.mode_type << 12) | e.mode_perms
        out += mode.to_bytes(4, "big")
        out += e.uid.to_bytes(4, "big")
        out += e.gid.to_bytes(4, "big")
        out += e.fsize.to_bytes(4, "big")
        out += int(e.sha, 16).to_bytes(20, "big")
        flags = (0x8000 if e.flag_assume_valid else 0) | (e.flag_stage << 12) | len(e.name.encode("utf-8"))
        out += flags.to_bytes(2, "big")
        out += e.name.encode("utf-8") + b"\x00"
        pos += 62 + len(e.name.encode("utf-8")) + 1
        # pad to 8-byte boundary
        if pos % 8:
            pad = 8 - (pos % 8)
            out += b"\x00" * pad
            pos += pad
    with open(repo_file(repo, "index"), "wb") as f:
        f.write(out)