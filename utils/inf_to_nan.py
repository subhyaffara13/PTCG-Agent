
def inf_to_nan(func):
    """Decorate function to return nan if it returns inf"""
    def wrap(*a, **kw):
        v = func(*a, **kw)
        if not np.isfinite(v):
            return np.nan
        return v
    return wrap

