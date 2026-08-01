
def _validate_sos(sos, xp=None):
    """Helper to validate a SOS input"""
    if xp is None:
        xp = np    # backcompat, cf sosfilt, sosfiltfilt

    sos = xp.asarray(sos)
    sos = xpx.atleast_nd(sos, ndim=2, xp=xp)
    if sos.ndim != 2:
        raise ValueError('sos array must be 2D')
    n_sections, m = sos.shape
    if m != 6:
        raise ValueError('sos array must be shape (n_sections, 6)')
    if not xp.all(sos[:, 3] == 1):
        raise ValueError('sos[:, 3] should be all ones')
    return sos, n_sections

