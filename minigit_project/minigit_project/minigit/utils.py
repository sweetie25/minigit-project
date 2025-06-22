def kvlm_parse(raw, start=0, dct=None):
    """
    Parse a key-value list with message (used by commits and tags).
    Returns a dict mapping keys→bytes (or key=None→message body).
    """
    if dct is None:
        dct = {}
    spc = raw.find(b" ", start)
    nl  = raw.find(b"\n", start)
    # end of headers
    if spc < 0 or nl < spc:
        assert nl == start
        dct[None] = raw[start+1:]
        return dct
    key = raw[start:spc]
    end = start
    # multiline values
    while True:
        end = raw.find(b"\n", end+1)
        if raw[end+1] != ord(" "):
            break
    val = raw[spc+1:end].replace(b"\n ", b"\n")
    if key in dct:
        if isinstance(dct[key], list):
            dct[key].append(val)
        else:
            dct[key] = [dct[key], val]
    else:
        dct[key] = val
    return kvlm_parse(raw, end+1, dct)

def kvlm_serialize(kvlm):
    """
    Serialize a dict produced by kvlm_parse back into bytes.
    """
    out = b""
    for k, v in kvlm.items():
        if k is None:
            continue
        vals = v if isinstance(v, list) else [v]
        for item in vals:
            # fold newlines
            folded = item.replace(b"\n", b"\n ")
            out += k + b" " + folded + b"\n"
    out += b"\n" + kvlm[None]
    return out
