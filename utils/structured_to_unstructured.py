import copy

def structured_to_unstructured(arr, dtype=None, copy=False, casting='unsafe'):
    """
    Converts an n-D structured array into an (n+1)-D unstructured array.

    The new array will have a new last dimension equal in size to the
    number of field-elements of the input array. If not supplied, the output
    datatype is determined from the numpy type promotion rules applied to all
    the field datatypes.

    Nested fields, as well as each element of any subarray fields, all count
    as a single field-elements.

    Parameters
    ----------
    arr : ndarray
       Structured array or dtype to convert. Cannot contain object datatype.
    dtype : dtype, optional
       The dtype of the output unstructured array.
    copy : bool, optional
        If true, always return a copy. If false, a view is returned if
        possible, such as when the `dtype` and strides of the fields are
        suitable and the array subtype is one of `numpy.ndarray`,
        `numpy.recarray` or `numpy.memmap`.

        .. versionchanged:: 1.25.0
            A view can now be returned if the fields are separated by a
            uniform stride.

    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        See casting argument of `numpy.ndarray.astype`. Controls what kind of
        data casting may occur.

    Returns
    -------
    unstructured : ndarray
       Unstructured array with one more dimension.

    Examples
    --------
    >>> import numpy as np

    >>> from numpy.lib import recfunctions as rfn
    >>> a = np.zeros(4, dtype=[('a', 'i4'), ('b', 'f4,u2'), ('c', 'f4', 2)])
    >>> a
    array([(0, (0., 0), [0., 0.]), (0, (0., 0), [0., 0.]),
           (0, (0., 0), [0., 0.]), (0, (0., 0), [0., 0.])],
          dtype=[('a', '<i4'), ('b', [('f0', '<f4'), ('f1', '<u2')]), ('c', '<f4', (2,))])
    >>> rfn.structured_to_unstructured(a)
    array([[0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0.]])

    >>> b = np.array([(1, 2, 5), (4, 5, 7), (7, 8 ,11), (10, 11, 12)],
    ...              dtype=[('x', 'i4'), ('y', 'f4'), ('z', 'f8')])
    >>> np.mean(rfn.structured_to_unstructured(b[['x', 'z']]), axis=-1)
    array([ 3. ,  5.5,  9. , 11. ])

    """  # noqa: E501
    if arr.dtype.names is None:
        raise ValueError('arr must be a structured array')

    fields = _get_fields_and_offsets(arr.dtype)
    n_fields = len(fields)
    if n_fields == 0 and dtype is None:
        raise ValueError("arr has no fields. Unable to guess dtype")
    elif n_fields == 0:
        # too many bugs elsewhere for this to work now
        raise NotImplementedError("arr with no fields is not supported")

    dts, counts, offsets = zip(*fields)
    names = [f'f{n}' for n in range(n_fields)]

    if dtype is None:
        out_dtype = np.result_type(*[dt.base for dt in dts])
    else:
        out_dtype = np.dtype(dtype)

    # Use a series of views and casts to convert to an unstructured array:

    # first view using flattened fields (doesn't work for object arrays)
    # Note: dts may include a shape for subarrays
    flattened_fields = np.dtype({'names': names,
                                 'formats': dts,
                                 'offsets': offsets,
                                 'itemsize': arr.dtype.itemsize})
    arr = arr.view(flattened_fields)

    # we only allow a few types to be unstructured by manipulating the
    # strides, because we know it won't work with, for example, np.matrix nor
    # np.ma.MaskedArray.
    can_view = type(arr) in (np.ndarray, np.recarray, np.memmap)
    if (not copy) and can_view and all(dt.base == out_dtype for dt in dts):
        # all elements have the right dtype already; if they have a common
        # stride, we can just return a view
        common_stride = _common_stride(offsets, counts, out_dtype.itemsize)
        if common_stride is not None:
            wrap = arr.__array_wrap__

            new_shape = arr.shape + (sum(counts), out_dtype.itemsize)
            new_strides = arr.strides + (abs(common_stride), 1)

            arr = arr[..., np.newaxis].view(np.uint8)  # view as bytes
            arr = arr[..., min(offsets):]  # remove the leading unused data
            arr = np.lib.stride_tricks.as_strided(arr,
                                                  new_shape,
                                                  new_strides,
                                                  subok=True)

            # cast and drop the last dimension again
            arr = arr.view(out_dtype)[..., 0]

            if common_stride < 0:
                arr = arr[..., ::-1]  # reverse, if the stride was negative
            if type(arr) is not type(wrap.__self__):
                # Some types (e.g. recarray) turn into an ndarray along the
                # way, so we have to wrap it again in order to match the
                # behavior with copy=True.
                arr = wrap(arr)
            return arr

    # next cast to a packed format with all fields converted to new dtype
    packed_fields = np.dtype({'names': names,
                              'formats': [(out_dtype, dt.shape) for dt in dts]})
    arr = arr.astype(packed_fields, copy=copy, casting=casting)

    # finally is it safe to view the packed fields as the unstructured type
    return arr.view((out_dtype, (sum(counts),)))

