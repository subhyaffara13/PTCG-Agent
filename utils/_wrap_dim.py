
def _wrap_dim(arg: Any, orig_ndim: int, allow_none: bool = True) -> DimEntry:
    """
    Convert various dimension representations to DimEntry.

    Args:
        arg: The argument to convert (Dim, int, or other)
        orig_ndim: Original number of dimensions
        allow_none: Whether to allow None values

    Returns:
        DimEntry representation of the dimension
    """
    from . import Dim

    if arg is None and allow_none:
        return DimEntry()  # None entry
    elif isinstance(arg, Dim):
        return DimEntry(arg)
    elif isinstance(arg, int):
        if arg < 0:
            pos = arg
        else:
            pos = arg - orig_ndim
        return DimEntry(pos)
    else:
        return DimEntry()


def _wrap_dim(dim: Any, ndim: int, keepdim: bool = False) -> DimEntry:
    """Convert single dimension specification to DimEntry object."""
    from . import Dim

    if isinstance(dim, Dim):
        if keepdim:
            raise ValueError("cannot preserve first-class dimensions with keepdim=True")
        return DimEntry(dim)
    elif isinstance(dim, int):
        i = dim
        while i >= 0:
            i -= ndim
        return DimEntry(i)
    else:
        return DimEntry()

