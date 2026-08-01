
def _merge_TTHinting(font, masterModel, master_ttfs):
    log.info("Merging TT hinting")
    assert "cvar" not in font

    # Check that the existing hinting is compatible

    # fpgm and prep table

    for tag in ("fpgm", "prep"):
        all_pgms = [m[tag].program for m in master_ttfs if tag in m]
        if not all_pgms:
            continue
        font_pgm = getattr(font.get(tag), "program", None)
        if any(pgm != font_pgm for pgm in all_pgms):
            log.warning(
                "Masters have incompatible %s tables, hinting is discarded." % tag
            )
            _remove_TTHinting(font)
            return

    # glyf table

    font_glyf = font["glyf"]
    master_glyfs = [m["glyf"] for m in master_ttfs]
    for name, glyph in font_glyf.glyphs.items():
        all_pgms = [getattr(glyf.get(name), "program", None) for glyf in master_glyfs]
        if not any(all_pgms):
            continue
        glyph.expand(font_glyf)
        font_pgm = getattr(glyph, "program", None)
        if any(pgm != font_pgm for pgm in all_pgms if pgm):
            log.warning(
                "Masters have incompatible glyph programs in glyph '%s', hinting is discarded."
                % name
            )
            # TODO Only drop hinting from this glyph.
            _remove_TTHinting(font)
            return

    # cvt table

    all_cvs = [Vector(m["cvt "].values) if "cvt " in m else None for m in master_ttfs]

    nonNone_cvs = models.nonNone(all_cvs)
    if not nonNone_cvs:
        # There is no cvt table to make a cvar table from, we're done here.
        return

    if not models.allEqual(len(c) for c in nonNone_cvs):
        log.warning("Masters have incompatible cvt tables, hinting is discarded.")
        _remove_TTHinting(font)
        return

    variations = []
    deltas, supports = masterModel.getDeltasAndSupports(
        all_cvs, round=round
    )  # builtin round calls into Vector.__round__, which uses builtin round as we like
    for i, (delta, support) in enumerate(zip(deltas[1:], supports[1:])):
        if all(v == 0 for v in delta):
            continue
        var = TupleVariation(support, delta)
        variations.append(var)

    # We can build the cvar table now.
    if variations:
        cvar = font["cvar"] = newTable("cvar")
        cvar.version = 1
        cvar.variations = variations

