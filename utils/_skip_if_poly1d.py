
def _skip_if_poly1d(arg):
    return None if isinstance(arg, np.poly1d) else arg

