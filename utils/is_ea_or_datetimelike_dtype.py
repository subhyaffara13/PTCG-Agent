
def is_ea_or_datetimelike_dtype(dtype: DtypeObj | None) -> bool:
    """
    Check for ExtensionDtype, datetime64 dtype, or timedelta64 dtype.

    Notes
    -----
    Checks only for dtype objects, not dtype-castable strings or types.
    """
    return isinstance(dtype, ExtensionDtype) or (lib.is_np_dtype(dtype, "mM"))

