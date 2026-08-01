
def _gaminv(a, b):
    # Defined to facilitate comparison between translation and source
    # Matlab's `gaminv` is like `special.gammaincinv` but args are reversed
    return special.gammaincinv(b, a)

