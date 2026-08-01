
def remove_hints(cff, *, removeUnusedSubrs: bool = True):
    for fontname in cff.keys():
        font = cff[fontname]
        cs = font.CharStrings
        # This can be tricky, but doesn't have to. What we do is:
        #
        # - Run all used glyph charstrings and recurse into subroutines,
        # - For each charstring (including subroutines), if it has any
        #   of the hint stem operators, we mark it as such.
        #   Upon returning, for each charstring we note all the
        #   subroutine calls it makes that (recursively) contain a stem,
        # - Dropping hinting then consists of the following two ops:
        #   * Drop the piece of the program in each charstring before the
        #     last call to a stem op or a stem-calling subroutine,
        #   * Drop all hintmask operations.
        # - It's trickier... A hintmask right after hints and a few numbers
        #    will act as an implicit vstemhm. As such, we track whether
        #    we have seen any non-hint operators so far and do the right
        #    thing, recursively... Good luck understanding that :(
        css = set()
        for c in cs.values():
            c.decompile()
            subrs = getattr(c.private, "Subrs", [])
            decompiler = _DehintingT2Decompiler(
                css,
                subrs,
                c.globalSubrs,
                c.private.nominalWidthX,
                c.private.defaultWidthX,
                c.private,
            )
            decompiler.execute(c)
            c.width = decompiler.width
        for charstring in css:
            _cs_drop_hints(charstring)
        del css

        # Drop font-wide hinting values
        all_privs = []
        if hasattr(font, "FDArray"):
            all_privs.extend(fd.Private for fd in font.FDArray)
        else:
            all_privs.append(font.Private)
        for priv in all_privs:
            for k in [
                "BlueValues",
                "OtherBlues",
                "FamilyBlues",
                "FamilyOtherBlues",
                "BlueScale",
                "BlueShift",
                "BlueFuzz",
                "StemSnapH",
                "StemSnapV",
                "StdHW",
                "StdVW",
                "ForceBold",
                "LanguageGroup",
                "ExpansionFactor",
            ]:
                if hasattr(priv, k):
                    setattr(priv, k, None)
    if removeUnusedSubrs:
        remove_unused_subroutines(cff)


def remove_hints(self):
    self.cff.remove_hints()

