
def _covhelper(x, y=None, rowvar=True, allow_masked=True):
    """
    Private function for the computation of covariance and correlation
    coefficients.

    """
    x = ma.array(x, ndmin=2, copy=True, dtype=float)
    xmask = ma.getmaskarray(x)
    # Quick exit if we can't process masked data
    if not allow_masked and xmask.any():
        raise ValueError("Cannot process masked data.")
    #
    if x.shape[0] == 1:
        rowvar = True
    # Make sure that rowvar is either 0 or 1
    rowvar = int(bool(rowvar))
    axis = 1 - rowvar
    if rowvar:
        tup = (slice(None), None)
    else:
        tup = (None, slice(None))
    #
    if y is None:
        # Check if we can guarantee that the integers in the (N - ddof)
        # normalisation can be accurately represented with single-precision
        # before computing the dot product.
        if x.shape[0] > 2 ** 24 or x.shape[1] > 2 ** 24:
            xnm_dtype = np.float64
        else:
            xnm_dtype = np.float32
        xnotmask = np.logical_not(xmask).astype(xnm_dtype)
    else:
        y = array(y, copy=False, ndmin=2, dtype=float)
        ymask = ma.getmaskarray(y)
        if not allow_masked and ymask.any():
            raise ValueError("Cannot process masked data.")
        if xmask.any() or ymask.any():
            if y.shape == x.shape:
                # Define some common mask
                common_mask = np.logical_or(xmask, ymask)
                if common_mask is not nomask:
                    xmask = x._mask = y._mask = ymask = common_mask
                    x._sharedmask = False
                    y._sharedmask = False
        x = ma.concatenate((x, y), axis)
        # Check if we can guarantee that the integers in the (N - ddof)
        # normalisation can be accurately represented with single-precision
        # before computing the dot product.
        if x.shape[0] > 2 ** 24 or x.shape[1] > 2 ** 24:
            xnm_dtype = np.float64
        else:
            xnm_dtype = np.float32
        xnotmask = np.logical_not(np.concatenate((xmask, ymask), axis)).astype(
            xnm_dtype
        )
    x -= x.mean(axis=rowvar)[tup]
    return (x, xnotmask, rowvar)

