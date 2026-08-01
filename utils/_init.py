
def _init():
    for code, titles in _codes.items():
        for title in titles:
            setattr(codes, title, code)
            if not title.startswith(("\\", "/")):
                setattr(codes, title.upper(), code)

    def doc(code: int) -> str:
        names = ", ".join(f"``{n}``" for n in _codes[code])
        return "* %d: %s" % (code, names)

    global __doc__
    __doc__ = (
        __doc__ + "\n" + "\n".join(doc(code) for code in sorted(_codes))
        if __doc__ is not None
        else None
    )


def _init() -> None:
    r"""Register prims as implementation of var_mean and group_norm."""
    global _lib

    if _lib is not None or not is_built():
        return

    from torch._decomp.decompositions import native_group_norm_backward
    from torch._refs import native_group_norm

    _lib = _Library("aten", "IMPL")  # noqa: TOR901
    _lib.impl("native_group_norm", native_group_norm, "MPS")
    _lib.impl("native_group_norm_backward", native_group_norm_backward, "MPS")


def _init():
    for code, titles in _codes.items():
        for title in titles:
            setattr(codes, title, code)
            if not title.startswith(("\\", "/")):
                setattr(codes, title.upper(), code)

    def doc(code):
        names = ", ".join(f"``{n}``" for n in _codes[code])
        return "* %d: %s" % (code, names)

    global __doc__
    __doc__ = (
        __doc__ + "\n" + "\n".join(doc(code) for code in sorted(_codes))
        if __doc__ is not None
        else None
    )

