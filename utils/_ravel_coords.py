
def _ravel_coords(coords, shape, order='C'):
    """Like np.ravel_multi_index, but avoids some overflow issues."""
    if len(coords) == 1:
        return coords[0]
    # Handle overflow as in https://github.com/scipy/scipy/pull/9132
    if len(coords) == 2:
        nrows, ncols = shape
        row, col = coords
        if order == 'C':
            maxval = (ncols * max(0, nrows - 1) + max(0, ncols - 1))
            idx_dtype = get_index_dtype(maxval=maxval)
            return np.multiply(ncols, row, dtype=idx_dtype) + col
        elif order == 'F':
            maxval = (nrows * max(0, ncols - 1) + max(0, nrows - 1))
            idx_dtype = get_index_dtype(maxval=maxval)
            return np.multiply(nrows, col, dtype=idx_dtype) + row
        else:
            raise ValueError("'order' must be 'C' or 'F'")
    return np.ravel_multi_index(coords, shape, order=order)

