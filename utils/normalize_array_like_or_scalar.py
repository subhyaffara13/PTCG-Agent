
def normalize_array_like_or_scalar(x, parm=None):  # codespell:ignore
    if _dtypes_impl.is_scalar_or_symbolic(x):
        return x
    return normalize_array_like(x, parm)  # codespell:ignore

