
def _has_infs(result) -> bool:
    if isinstance(result, np.ndarray):
        if result.dtype in ("f8", "f4"):
            # Note: outside of a nanops-specific test, we always have
            #  result.ndim == 1, so there is no risk of this ravel making a copy.
            return lib.has_infs(result.ravel("K"))
    try:
        return np.isinf(result).any()
    except (TypeError, NotImplementedError):
        # if it doesn't support infs, then it can't have infs
        return False

