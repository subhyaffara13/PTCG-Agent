
def _create_dimlist(name: str, size: int | list[int | None] | None = None) -> DimList:
    """Create a DimList object with the given name and optional size."""
    dimlist = DimList(name=name)
    if size is not None:
        if isinstance(size, int):
            dimlist.bind_len(size)
        else:
            # size is a list of optional ints
            dimlist.bind_len(len(size))
            for i, s in enumerate(size):
                if s is not None:
                    dimlist._dims[i].size = s
    return dimlist

