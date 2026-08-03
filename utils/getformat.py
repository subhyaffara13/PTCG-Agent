import re

def getformat(fmt, keep_pad_byte=False):
    fmt = tostr(fmt, encoding="ascii")
    try:
        formatstring, names, fixes = _formatcache[fmt]
    except KeyError:
        lines = re.split("[\n;]", fmt)
        formatstring = ""
        names = {}
        fixes = {}
        for line in lines:
            if _emptyRE.match(line):
                continue
            m = _extraRE.match(line)
            if m:
                formatchar = m.group(1)
                if formatchar != "x" and formatstring:
                    raise Error("a special fmt char must be first")
            else:
                m = _elementRE.match(line)
                if not m:
                    raise Error("syntax error in fmt: '%s'" % line)
                name = m.group(1)
                formatchar = m.group(2)
                if keep_pad_byte or formatchar != "x":
                    names[name] = formatchar
                if m.group(3):
                    # fixed point
                    before = int(m.group(3))
                    after = int(m.group(4))
                    bits = before + after
                    if bits not in [8, 16, 32]:
                        raise Error("fixed point must be 8, 16 or 32 bits long")
                    formatchar = _fixedpointmappings[bits]
                    names[name] = formatchar
                    assert m.group(5) == "F"
                    fixes[name] = after
            formatstring += formatchar
        _formatcache[fmt] = formatstring, names, fixes
    return formatstring, names, fixes

