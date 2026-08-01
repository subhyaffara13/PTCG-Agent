
def almost(a, b, decimal=6, fill_value=True):
    """
    Returns True if a and b are equal up to decimal places.

    If fill_value is True, masked values considered equal. Otherwise,
    masked values are considered unequal.

    """
    m = mask_or(getmask(a), getmask(b))
    d1 = filled(a)
    d2 = filled(b)
    if d1.dtype.char == "O" or d2.dtype.char == "O":
        return np.equal(d1, d2).ravel()
    x = filled(
        masked_array(d1, copy=False, mask=m), fill_value
    ).astype(np.float64)
    y = filled(masked_array(d2, copy=False, mask=m), 1).astype(np.float64)
    d = np.around(np.abs(x - y), decimal) <= 10.0 ** (-decimal)
    return d.ravel()

