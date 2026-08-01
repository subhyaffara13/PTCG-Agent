
def _tolerance_variants(notation: str) -> set[str]:
    """Generate forgiving lookup keys for ``*`` and trailing ``Pass``.

    OpenSpiel encodes hits with ``*`` and unused-die markers with ``Pass``
    appended to the move (e.g. ``Bar/24 Pass``). Models routinely omit one
    or both because they feel like cosmetic annotations. Treat them as
    optional on both sides of the match so the model's intent gets through.
    """
    variants = {notation, notation.replace("*", "")}
    for v in list(variants):
        if v.endswith(_PASS_SUFFIX):
            variants.add(v[: -len(_PASS_SUFFIX)].strip())
    return {v for v in variants if v}

