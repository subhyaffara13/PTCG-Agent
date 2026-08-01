
def morphological_laplace(input, size=None, footprint=None, structure=None,
                          output=None, mode="reflect", cval=0.0, origin=0, *,
                          axes=None):
    """
    Multidimensional morphological laplace.

    Parameters
    ----------
    input : array_like
        Input.
    size : tuple of ints
        Shape of a flat and full structuring element used for the mathematical
        morphology operations. Optional if `footprint` or `structure` is
        provided.
    footprint : array of ints, optional
        Positions of non-infinite elements of a flat structuring element
        used for the morphology operations.
    structure : array of ints, optional
        Structuring element used for the morphology operations. `structure` may
        be a non-flat structuring element. The `structure` array applies
        offsets to the pixels in a neighborhood (the offset is additive during
        dilation and subtractive during erosion)
    output : ndarray, optional
        An output array can optionally be provided.
    mode : {'reflect','constant','nearest','mirror', 'wrap'}, optional
        The mode parameter determines how the array borders are handled.
        For 'constant' mode, values beyond borders are set to be `cval`.
        Default is 'reflect'.
    cval : scalar, optional
        Value to fill past edges of input if mode is 'constant'.
        Default is 0.0
    origin : origin, optional
        The origin parameter controls the placement of the filter.
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    morphological_laplace : ndarray
        Output

    """
    input = np.asarray(input)
    tmp1 = grey_dilation(input, size, footprint, structure, None, mode,
                         cval, origin, axes=axes)
    if isinstance(output, np.ndarray):
        grey_erosion(input, size, footprint, structure, output, mode,
                     cval, origin, axes=axes)
        np.add(tmp1, output, output)
        np.subtract(output, input, output)
        return np.subtract(output, input, output)
    else:
        tmp2 = grey_erosion(input, size, footprint, structure, None, mode,
                            cval, origin, axes=axes)
        np.add(tmp1, tmp2, tmp2)
        np.subtract(tmp2, input, tmp2)
        np.subtract(tmp2, input, tmp2)
        return tmp2

