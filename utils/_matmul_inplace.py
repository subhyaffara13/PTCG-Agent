
def _matmul_inplace(x, y, verbosityLevel=0):
    """Perform 'np.matmul' in-place if possible.

    If some sufficient conditions for inplace matmul are met, do so.
    Otherwise try inplace update and fall back to overwrite if that fails.
    """
    if x.flags["CARRAY"] and x.shape[1] == y.shape[1] and x.dtype == y.dtype:
        # conditions where we can guarantee that inplace updates will work;
        # i.e. x is not a view/slice, x & y have compatible dtypes, and the
        # shape of the result of x @ y matches the shape of x.
        np.matmul(x, y, out=x)
    else:
        # ideally, we'd have an exhaustive list of conditions above when
        # inplace updates are possible; since we don't, we opportunistically
        # try if it works, and fall back to overwriting if necessary
        try:
            np.matmul(x, y, out=x)
        except Exception:
            if verbosityLevel:
                warnings.warn(
                    "Inplace update of x = x @ y failed, "
                    "x needs to be overwritten.",
                    UserWarning, stacklevel=3
                )
            x = x @ y
    return x

