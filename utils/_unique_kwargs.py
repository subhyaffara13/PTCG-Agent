
def _unique_kwargs(xp: Namespace) -> dict[str, bool]:
    # Older versions of NumPy and CuPy do not have equal_nan. Rather than
    # trying to parse version numbers, just check if equal_nan is in the
    # signature.
    s = inspect.signature(xp.unique)
    if "equal_nan" in s.parameters:
        return {"equal_nan": False}
    return {}

