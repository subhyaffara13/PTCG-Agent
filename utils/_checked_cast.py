
def _checked_cast(ty: type[_T], obj: object) -> _T:
    if not isinstance(obj, ty):
        raise AssertionError(f"expected {ty} but got {type(obj)}")
    return obj

