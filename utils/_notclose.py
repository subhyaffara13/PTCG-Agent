
def _notclose(fs, rtol=_rtol, atol=_xtol):
    # Ensure not None, not 0, all finite, and not very close to each other
    notclosefvals = (
            all(fs) and all(np.isfinite(fs)) and
            not any(any(np.isclose(_f, fs[i + 1:], rtol=rtol, atol=atol))
                    for i, _f in enumerate(fs[:-1])))
    return notclosefvals

