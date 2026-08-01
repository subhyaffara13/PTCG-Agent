
def isidentifier(s: str) -> bool:
    warn(
        "traitlets.traitlets.isidentifier(s) is deprecated since traitlets 5.14.4 Use `s.isidentifier()`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return s.isidentifier()

