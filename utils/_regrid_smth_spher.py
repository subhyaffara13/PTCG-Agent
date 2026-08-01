
def _regrid_smth_spher(iopt, ider, u, v, r, r0, r1, s, nuest, nvest, eps):
    """
    Wrapper for spgrid (smoothing on spherical grid).
    Returns: nu, tu, nv, tv, c, fp, ier

    Note: eps parameter is not used by the C implementation but kept for
    legacy API compatibility.
    """
    u = np.ascontiguousarray(u, dtype=np.float64)
    v = np.ascontiguousarray(v, dtype=np.float64)
    r = np.ascontiguousarray(r, dtype=np.float64)
    iopt = np.ascontiguousarray(iopt, dtype=np.int32)
    ider = np.ascontiguousarray(ider, dtype=np.int32)

    # Handle None values for r0 and r1 (only used when ider indicates they should be)
    if r0 is None:
        r0 = 0.0
    if r1 is None:
        r1 = 0.0

    # Call spgrid - workspace arrays are now allocated internally in C
    nu, tu, nv, tv, c, fp, ier = _fitpack.spgrid(
        iopt, ider, u, v, r, r0, r1, s, nuest, nvest)

    return nu, tu, nv, tv, c, fp, ier

