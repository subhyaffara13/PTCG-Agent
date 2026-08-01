
def AxisRange(minimum, maximum):
    warnings.warn(
        "AxisRange is deprecated; use AxisTriple instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return AxisTriple(minimum, None, maximum)

