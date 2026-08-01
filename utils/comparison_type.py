
def comparison_type(logical_line, noqa):
    r"""Object type comparisons should `is` / `is not` / `isinstance()`.

    Do not compare types directly.

    Okay: if isinstance(obj, int):
    Okay: if type(obj) is int:
    E721: if type(obj) == type(1):
    """
    match = COMPARE_TYPE_REGEX.search(logical_line)
    if match and not noqa:
        inst = match.group(1)
        if inst and inst.isidentifier() and inst not in SINGLETONS:
            return  # Allow comparison for types which are not obvious
        yield (
            match.start(),
            "E721 do not compare types, for exact checks use `is` / `is not`, "
            "for instance checks use `isinstance()`",
        )

