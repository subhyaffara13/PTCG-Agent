
def normalize_optional_array_like(x, parm=None):  # codespell:ignore
    # This explicit normalizer is needed because otherwise normalize_array_like
    # does not run for a parameter annotated as Optional[ArrayLike]
    return None if x is None else normalize_array_like(x, parm)  # codespell:ignore

