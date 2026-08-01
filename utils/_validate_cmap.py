
def _validate_cmap(s):
    _api.check_isinstance((str, Colormap), cmap=s)
    return s

