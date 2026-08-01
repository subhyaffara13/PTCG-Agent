
def normalize_casting(arg, parm=None):  # codespell:ignore
    if arg not in ["no", "equiv", "safe", "same_kind", "unsafe"]:
        raise ValueError(
            f"casting must be one of 'no', 'equiv', 'safe', 'same_kind', or 'unsafe' (got '{arg}')"
        )
    return arg

