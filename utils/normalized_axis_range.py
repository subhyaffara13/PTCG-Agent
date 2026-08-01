
def NormalizedAxisRange(minimum, maximum):
    warnings.warn(
        "NormalizedAxisRange is deprecated; use AxisTriple instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return NormalizedAxisTriple(minimum, None, maximum)

