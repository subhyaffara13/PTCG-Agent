
def affine_transform(input, matrix, offset=0.0, output_shape=None,
                     output=None, order=3,
                     mode='constant', cval=0.0, prefilter=True):
    """
    Apply an affine transformation.

    Given an output image pixel index vector ``o``, the pixel value
    is determined from the input image at position
    ``np.dot(matrix, o) + offset``.

    This does 'pull' (or 'backward') resampling, transforming the output space
    to the input to locate data. Affine transformations are often described in
    the 'push' (or 'forward') direction, transforming input to output. If you
    have a matrix for the 'push' transformation, use its inverse
    (:func:`numpy.linalg.inv`) in this function.

    Parameters
    ----------
    %(input)s
    matrix : ndarray
        The inverse coordinate transformation matrix, mapping output
        coordinates to input coordinates. If ``ndim`` is the number of
        dimensions of ``input``, the given matrix must have one of the
        following shapes:

        - ``(ndim, ndim)``: the linear transformation matrix for each
          output coordinate.
        - ``(ndim,)``: assume that the 2-D transformation matrix is
          diagonal, with the diagonal specified by the given value. A more
          efficient algorithm is then used that exploits the separability
          of the problem.
        - ``(ndim + 1, ndim + 1)``: assume that the transformation is
          specified using homogeneous coordinates [1]_. In this case, any
          value passed to ``offset`` is ignored.
        - ``(ndim, ndim + 1)``: as above, but the bottom row of a
          homogeneous transformation matrix is always ``[0, 0, ..., 1]``,
          and may be omitted.

    offset : float or sequence, optional
        The offset into the array where the transform is applied. If a float,
        `offset` is the same for each axis. If a sequence, `offset` should
        contain one value for each axis.
    output_shape : tuple of ints, optional
        Shape tuple.
    %(output)s
    order : int, optional
        The order of the spline interpolation, default is 3.
        The order has to be in the range 0-5.
    %(mode_interp_constant)s
    %(cval)s
    %(prefilter)s

    Returns
    -------
    affine_transform : ndarray
        The transformed input.

    Examples
    --------
    Use `affine_transform` to stretch an image::

    >>> from scipy.ndimage import affine_transform
    >>> from scipy.datasets import face
    >>> from matplotlib import pyplot as plt
    >>> import numpy as np
    >>> im = face(gray=True)
    >>> matrix = (0.5, 2)
    >>> im2 = affine_transform(im, matrix)
    >>> plt.imshow(im2)
    >>> plt.show()

    Rotate an image by 90 degrees and project it onto an expanded canvas::

    >>> matrix = ((0, 1), (1, 0))
    >>> im3 = affine_transform(im, matrix, output_shape=(1024, 1024))
    >>> plt.imshow(im3)
    >>> plt.show()

    Offset the rotation so that the image is centred::

    >>> output_shape = (1200, 1200)
    >>> offset = (np.array(im.shape) - output_shape) / 2
    >>> im4 = affine_transform(im, matrix, offset=offset, output_shape=output_shape)
    >>> plt.imshow(im4)
    >>> plt.show()

    Notes
    -----
    The given matrix and offset are used to find for each point in the
    output the corresponding coordinates in the input by an affine
    transformation. The value of the input at those coordinates is
    determined by spline interpolation of the requested order. Points
    outside the boundaries of the input are filled according to the given
    mode.

    .. versionchanged:: 0.18.0
        Previously, the exact interpretation of the affine transformation
        depended on whether the matrix was supplied as a 1-D or a
        2-D array. If a 1-D array was supplied
        to the matrix parameter, the output pixel value at index ``o``
        was determined from the input image at position
        ``matrix * (o + offset)``.

    For complex-valued `input`, this function transforms the real and imaginary
    components independently.

    .. versionadded:: 1.6.0
        Complex-valued support added.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Homogeneous_coordinates
    """
    if order < 0 or order > 5:
        raise RuntimeError('spline order not supported')
    input = np.asarray(input)
    if output_shape is None:
        if isinstance(output, np.ndarray):
            output_shape = output.shape
        else:
            output_shape = input.shape
    if input.ndim < 1 or len(output_shape) < 1:
        raise RuntimeError('input and output rank must be > 0')
    complex_output = np.iscomplexobj(input)
    output = _ni_support._get_output(output, input, shape=output_shape,
                                     complex_output=complex_output)
    if complex_output:
        kwargs = dict(offset=offset, output_shape=output_shape, order=order,
                      mode=mode, prefilter=prefilter)
        affine_transform(input.real, matrix, output=output.real,
                         cval=np.real(cval), **kwargs)
        affine_transform(input.imag, matrix, output=output.imag,
                         cval=np.imag(cval), **kwargs)
        return output
    if prefilter and order > 1:
        padded, npad = _prepad_for_spline_filter(input, mode, cval)
        filtered = spline_filter(padded, order, output=np.float64, mode=mode)
    else:
        npad = 0
        filtered = input
    mode = _ni_support._extend_mode_to_code(mode)
    matrix = np.asarray(matrix, dtype=np.float64)
    if matrix.ndim not in [1, 2] or matrix.shape[0] < 1:
        raise RuntimeError('no proper affine matrix provided')
    if (matrix.ndim == 2 and matrix.shape[1] == input.ndim + 1 and
            (matrix.shape[0] in [input.ndim, input.ndim + 1])):
        if matrix.shape[0] == input.ndim + 1:
            exptd = [0] * input.ndim + [1]
            if not np.all(matrix[input.ndim] == exptd):
                msg = (f'Expected homogeneous transformation matrix with '
                       f'shape {matrix.shape} for image shape {input.shape}, '
                       f'but bottom row was not equal to {exptd}')
                raise ValueError(msg)
        # assume input is homogeneous coordinate transformation matrix
        offset = matrix[:input.ndim, input.ndim]
        matrix = matrix[:input.ndim, :input.ndim]
    if matrix.shape[0] != input.ndim:
        raise RuntimeError('affine matrix has wrong number of rows')
    if matrix.ndim == 2 and matrix.shape[1] != output.ndim:
        raise RuntimeError('affine matrix has wrong number of columns')
    if not matrix.flags.contiguous:
        matrix = matrix.copy()
    offset = _ni_support._normalize_sequence(offset, input.ndim)
    offset = np.asarray(offset, dtype=np.float64)
    if offset.ndim != 1 or offset.shape[0] < 1:
        raise RuntimeError('no proper offset provided')
    if not offset.flags.contiguous:
        offset = offset.copy()
    if matrix.ndim == 1:
        _nd_image.zoom_shift(filtered, matrix, offset/matrix, output, order,
                             mode, cval, npad, False)
    else:
        _nd_image.geometric_transform(filtered, None, None, matrix, offset,
                                      output, order, mode, cval, npad, None,
                                      None)
    return output

