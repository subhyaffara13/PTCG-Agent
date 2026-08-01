
def _index_to_interp_indices(index: Index, method: str) -> np.ndarray:
    """
    Convert Index to ndarray of indices to pass to NumPy/SciPy.
    """
    xarr = index._values
    if needs_i8_conversion(xarr.dtype):
        # GH#1646 for dt64tz
        xarr = xarr.view("i8")

    if method == "linear":
        inds = xarr
        inds = cast(np.ndarray, inds)
    else:
        inds = np.asarray(xarr)

        if method in ("values", "index"):
            if inds.dtype == np.object_:
                inds = lib.maybe_convert_objects(inds)

    return inds

