
def pep508_versionspec(value: str) -> bool:
    """Expression that can be used to specify/lock versions (including ranges)
    See ``versionspec`` in :ref:`PyPA's dependency specifiers
    <pypa:dependency-specifiers>` (initially introduced in :pep:`508`).
    """
    if any(c in value for c in (";", "]", "@")):
        # In PEP 508:
        # conditional markers, extras and URL specs are not included in the
        # versionspec
        return False
    # Let's pretend we have a dependency called `requirement` with the given
    # version spec, then we can reuse the pep508 function for validation:
    return pep508(f"requirement{value}")

