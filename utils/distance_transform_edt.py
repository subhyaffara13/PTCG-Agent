
def distance_transform_edt(input, sampling=None, return_distances=True,
                           return_indices=False, distances=None, indices=None):
    """
    Exact Euclidean distance transform.

    This function calculates the distance transform of the `input`, by
    replacing each foreground (non-zero) element, with its
    shortest distance to the background (any zero-valued element).

    In addition to the distance transform, the feature transform can
    be calculated. In this case the index of the closest background
    element to each foreground element is returned in a separate array.

    Parameters
    ----------
    input : array_like
        Input data to transform. Can be any type but will be converted
        into binary: 1 wherever input equates to True, 0 elsewhere.
    sampling : float, or sequence of float, optional
        Spacing of elements along each dimension. If a sequence, must be of
        length equal to the input rank; if a single number, this is used for
        all axes. If not specified, a grid spacing of unity is implied.
    return_distances : bool, optional
        Whether to calculate the distance transform.
        Default is True.
    return_indices : bool, optional
        Whether to calculate the feature transform.
        Default is False.
    distances : float64 ndarray, optional
        An output array to store the calculated distance transform, instead of
        returning it.
        `return_distances` must be True.
        It must be the same shape as `input`.
    indices : int32 ndarray, optional
        An output array to store the calculated feature transform, instead of
        returning it.
        `return_indices` must be True.
        Its shape must be ``(input.ndim,) + input.shape``.

    Returns
    -------
    distances : float64 ndarray, optional
        The calculated distance transform. Returned only when
        `return_distances` is True and `distances` is not supplied.
        It will have the same shape as the input array.
    indices : int32 ndarray, optional
        The calculated feature transform. It has an input-shaped array for each
        dimension of the input. See example below.
        Returned only when `return_indices` is True and `indices` is not
        supplied.

    Notes
    -----
    The Euclidean distance transform gives values of the Euclidean
    distance::

                    n
      y_i = sqrt(sum (x[i]-b[i])**2)
                    i

    where b[i] is the background point (value 0) with the smallest
    Euclidean distance to input points x[i], and n is the
    number of dimensions.

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.array(([0,1,1,1,1],
    ...               [0,0,1,1,1],
    ...               [0,1,1,1,1],
    ...               [0,1,1,1,0],
    ...               [0,1,1,0,0]))
    >>> ndimage.distance_transform_edt(a)
    array([[ 0.    ,  1.    ,  1.4142,  2.2361,  3.    ],
           [ 0.    ,  0.    ,  1.    ,  2.    ,  2.    ],
           [ 0.    ,  1.    ,  1.4142,  1.4142,  1.    ],
           [ 0.    ,  1.    ,  1.4142,  1.    ,  0.    ],
           [ 0.    ,  1.    ,  1.    ,  0.    ,  0.    ]])

    With a sampling of 2 units along x, 1 along y:

    >>> ndimage.distance_transform_edt(a, sampling=[2,1])
    array([[ 0.    ,  1.    ,  2.    ,  2.8284,  3.6056],
           [ 0.    ,  0.    ,  1.    ,  2.    ,  3.    ],
           [ 0.    ,  1.    ,  2.    ,  2.2361,  2.    ],
           [ 0.    ,  1.    ,  2.    ,  1.    ,  0.    ],
           [ 0.    ,  1.    ,  1.    ,  0.    ,  0.    ]])

    Asking for indices as well:

    >>> edt, inds = ndimage.distance_transform_edt(a, return_indices=True)
    >>> inds
    array([[[0, 0, 1, 1, 3],
            [1, 1, 1, 1, 3],
            [2, 2, 1, 3, 3],
            [3, 3, 4, 4, 3],
            [4, 4, 4, 4, 4]],
           [[0, 0, 1, 1, 4],
            [0, 1, 1, 1, 4],
            [0, 0, 1, 4, 4],
            [0, 0, 3, 3, 4],
            [0, 0, 3, 3, 4]]], dtype=int32)

    With arrays provided for inplace outputs:

    >>> indices = np.zeros(((np.ndim(a),) + a.shape), dtype=np.int32)
    >>> ndimage.distance_transform_edt(a, return_indices=True, indices=indices)
    array([[ 0.    ,  1.    ,  1.4142,  2.2361,  3.    ],
           [ 0.    ,  0.    ,  1.    ,  2.    ,  2.    ],
           [ 0.    ,  1.    ,  1.4142,  1.4142,  1.    ],
           [ 0.    ,  1.    ,  1.4142,  1.    ,  0.    ],
           [ 0.    ,  1.    ,  1.    ,  0.    ,  0.    ]])
    >>> indices
    array([[[0, 0, 1, 1, 3],
            [1, 1, 1, 1, 3],
            [2, 2, 1, 3, 3],
            [3, 3, 4, 4, 3],
            [4, 4, 4, 4, 4]],
           [[0, 0, 1, 1, 4],
            [0, 1, 1, 1, 4],
            [0, 0, 1, 4, 4],
            [0, 0, 3, 3, 4],
            [0, 0, 3, 3, 4]]], dtype=int32)

    """
    ft_inplace = isinstance(indices, np.ndarray)
    dt_inplace = isinstance(distances, np.ndarray)
    _distance_transform_arg_check(
        dt_inplace, ft_inplace, return_distances, return_indices
    )

    # calculate the feature transform
    input = np.atleast_1d(np.where(input, 1, 0).astype(np.int8))
    if sampling is not None:
        sampling = _ni_support._normalize_sequence(sampling, input.ndim)
        sampling = np.asarray(sampling, dtype=np.float64)
        if not sampling.flags.contiguous:
            sampling = sampling.copy()

    if ft_inplace:
        ft = indices
        if ft.shape != (input.ndim,) + input.shape:
            raise RuntimeError('indices array has wrong shape')
        if ft.dtype.type != np.int32:
            raise RuntimeError('indices array must be int32')
    else:
        ft = np.zeros((input.ndim,) + input.shape, dtype=np.int32)

    _nd_image.euclidean_feature_transform(input, sampling, ft)
    # if requested, calculate the distance transform
    if return_distances:
        dt = ft - np.indices(input.shape, dtype=ft.dtype)
        dt = dt.astype(np.float64)
        if sampling is not None:
            for ii in range(len(sampling)):
                dt[ii, ...] *= sampling[ii]
        np.multiply(dt, dt, dt)
        if dt_inplace:
            dt = np.add.reduce(dt, axis=0)
            if distances.shape != dt.shape:
                raise RuntimeError('distances array has wrong shape')
            if distances.dtype.type != np.float64:
                raise RuntimeError('distances array must be float64')
            np.sqrt(dt, distances)
        else:
            dt = np.add.reduce(dt, axis=0)
            dt = np.sqrt(dt)

    # construct and return the result
    result = []
    if return_distances and not dt_inplace:
        result.append(dt)
    if return_indices and not ft_inplace:
        result.append(ft)

    if len(result) == 2:
        return tuple(result)
    elif len(result) == 1:
        return result[0]
    else:
        return None

