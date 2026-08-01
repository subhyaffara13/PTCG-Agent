
def _include_extra(req: str, extra: str, condition: str) -> Requirement:
    r = Requirement(req)  # create a fresh object that can be modified
    parts = (
        f"({r.marker})" if r.marker else None,
        f"({condition})" if condition else None,
        f"extra == {extra!r}" if extra else None,
    )
    r.marker = Marker(" and ".join(x for x in parts if x))
    return r

