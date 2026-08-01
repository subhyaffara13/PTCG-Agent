
def exception_to_nan(func):
    """Decorate function to return nan if it raises an exception"""
    def wrap(*a, **kw):
        try:
            return func(*a, **kw)
        except Exception:
            return np.nan
    return wrap

