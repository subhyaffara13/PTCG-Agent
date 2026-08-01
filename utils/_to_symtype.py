
def _to_symtype(t: type[bool]) -> type[SymBool]: ...


def _to_symtype(t: type[int]) -> type[SymInt]: ...


def _to_symtype(t: type[float]) -> type[SymFloat]: ...


def _to_symtype(t: type) -> type: ...


def _to_symtype(t: type) -> type:
    if t is bool:
        return SymBool
    if t is int:
        return SymInt
    if t is float:
        return SymFloat
    return t

