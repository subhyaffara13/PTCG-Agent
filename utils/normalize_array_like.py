
def normalize_array_like(x, parm=None):  # codespell:ignore
    from ._ndarray import asarray

    return asarray(x).tensor

