
def htmlentityreplace_errors(exc):
    if isinstance(exc, (UnicodeEncodeError, UnicodeTranslateError)):
        res = []
        codepoints = []
        skip = False
        for i, c in enumerate(exc.object[exc.start:exc.end]):
            if skip:
                skip = False
                continue
            index = i + exc.start
            if _utils.isSurrogatePair(exc.object[index:min([exc.end, index + 2])]):
                codepoint = _utils.surrogatePairToCodepoint(exc.object[index:index + 2])
                skip = True
            else:
                codepoint = ord(c)
            codepoints.append(codepoint)
        for cp in codepoints:
            e = _encode_entity_map.get(cp)
            if e:
                res.append("&")
                res.append(e)
                if not e.endswith(";"):
                    res.append(";")
            else:
                res.append("&#x%s;" % (hex(cp)[2:]))
        return ("".join(res), exc.end)
    else:
        return xmlcharrefreplace_errors(exc)

