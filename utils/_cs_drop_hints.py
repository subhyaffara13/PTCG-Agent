
def _cs_drop_hints(charstring):
    hints = charstring._hints

    if hints.deletions:
        p = charstring.program
        for idx in reversed(hints.deletions):
            del p[idx - 2 : idx]

    if hints.has_hint:
        assert not hints.deletions or hints.last_hint <= hints.deletions[0]
        charstring.program = charstring.program[hints.last_hint :]
        if not charstring.program:
            # TODO CFF2 no need for endchar.
            charstring.program.append("endchar")
        if hasattr(charstring, "width"):
            # Insert width back if needed
            if charstring.width != charstring.private.defaultWidthX:
                # For CFF2 charstrings, this should never happen
                assert (
                    charstring.private.defaultWidthX is not None
                ), "CFF2 CharStrings must not have an initial width value"
                charstring.program.insert(
                    0, charstring.width - charstring.private.nominalWidthX
                )

    if hints.has_hintmask:
        i = 0
        p = charstring.program
        while i < len(p):
            if p[i] in ["hintmask", "cntrmask"]:
                assert i + 1 <= len(p)
                del p[i : i + 2]
                continue
            i += 1

    assert len(charstring.program)

    del charstring._hints

