
def upfirdn_naive(x, h, up=1, down=1):
    """Naive upfirdn processing in Python.

    Note: arg order (x, h) differs to facilitate apply_along_axis use.
    """
    x = np.asarray(x)
    h = np.asarray(h)
    out = np.zeros(len(x) * up, x.dtype)
    out[::up] = x
    out = np.convolve(h, out)[::down][:_output_len(len(h), len(x), up, down)]
    return out

