
def _get_cs(charstrings, glyphName, filterEmpty=False):
    if glyphName not in charstrings:
        return None
    cs = charstrings[glyphName]

    if filterEmpty:
        cs.decompile()
        if cs.program == []:  # CFF2 empty charstring
            return None
        elif (
            len(cs.program) <= 2
            and cs.program[-1] == "endchar"
            and (len(cs.program) == 1 or type(cs.program[0]) in (int, float))
        ):  # CFF1 empty charstring
            return None

    return cs

