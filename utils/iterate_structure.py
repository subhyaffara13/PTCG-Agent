
def iterate_structure(structure, iterations, origin=None):
    """
    Iterate a structure by dilating it with itself.

    Parameters
    ----------
    structure : array_like
       Structuring element (an array of bools, for example), to be dilated with
       itself.
    iterations : int
       number of dilations performed on the structure with itself
    origin : optional
        If origin is None, only the iterated structure is returned. If
        not, a tuple of the iterated structure and the modified origin is
        returned.

    Returns
    -------
    iterate_structure : ndarray of bools
        A new structuring element obtained by dilating `structure`
        (`iterations` - 1) times with itself.

    See Also
    --------
    generate_binary_structure

    Examples
    --------
    >>> from scipy import ndimage
    >>> struct = ndimage.generate_binary_structure(2, 1)
    >>> struct.astype(int)
    array([[0, 1, 0],
           [1, 1, 1],
           [0, 1, 0]])
    >>> ndimage.iterate_structure(struct, 2).astype(int)
    array([[0, 0, 1, 0, 0],
           [0, 1, 1, 1, 0],
           [1, 1, 1, 1, 1],
           [0, 1, 1, 1, 0],
           [0, 0, 1, 0, 0]])
    >>> ndimage.iterate_structure(struct, 3).astype(int)
    array([[0, 0, 0, 1, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 1, 0, 0, 0]])

    """
    structure = np.asarray(structure)
    if iterations < 2:
        return structure.copy()
    ni = iterations - 1
    shape = [ii + ni * (ii - 1) for ii in structure.shape]
    pos = [ni * (structure.shape[ii] // 2) for ii in range(len(shape))]
    slc = tuple(slice(pos[ii], pos[ii] + structure.shape[ii], None)
                for ii in range(len(shape)))
    out = np.zeros(shape, bool)
    out[slc] = structure != 0
    out = binary_dilation(out, structure, iterations=ni)
    if origin is None:
        return out
    else:
        origin = _ni_support._normalize_sequence(origin, structure.ndim)
        origin = [iterations * o for o in origin]
        return out, origin

