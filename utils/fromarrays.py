
def fromarrays(arraylist, dtype=None, shape=None, formats=None,
               names=None, titles=None, aligned=False, byteorder=None,
               fill_value=None):
    """
    Creates a mrecarray from a (flat) list of masked arrays.

    Parameters
    ----------
    arraylist : sequence
        A list of (masked) arrays. Each element of the sequence is first converted
        to a masked array if needed. If a 2D array is passed as argument, it is
        processed line by line
    dtype : {None, dtype}, optional
        Data type descriptor.
    shape : {None, integer}, optional
        Number of records. If None, shape is defined from the shape of the
        first array in the list.
    formats : {None, sequence}, optional
        Sequence of formats for each individual field. If None, the formats will
        be autodetected by inspecting the fields and selecting the highest dtype
        possible.
    names : {None, sequence}, optional
        Sequence of the names of each field.
    fill_value : {None, sequence}, optional
        Sequence of data to be used as filling values.

    Notes
    -----
    Lists of tuples should be preferred over lists of lists for faster processing.

    """
    datalist = [ma.getdata(x) for x in arraylist]
    masklist = [np.atleast_1d(ma.getmaskarray(x)) for x in arraylist]
    _array = np.rec.fromarrays(datalist,
                               dtype=dtype, shape=shape, formats=formats,
                               names=names, titles=titles, aligned=aligned,
                               byteorder=byteorder).view(mrecarray)
    _array._mask.flat = list(zip(*masklist))
    if fill_value is not None:
        _array.fill_value = fill_value
    return _array


def fromarrays(arrayList, dtype=None, shape=None, formats=None,
               names=None, titles=None, aligned=False, byteorder=None):
    """Create a record array from a (flat) list of arrays

    Parameters
    ----------
    arrayList : list or tuple
        List of array-like objects (such as lists, tuples,
        and ndarrays).
    dtype : data-type, optional
        valid dtype for all arrays
    shape : int or tuple of ints, optional
        Shape of the resulting array. If not provided, inferred from
        ``arrayList[0]``.
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.rec.format_parser` to construct a dtype. See that function for
        detailed documentation.

    Returns
    -------
    np.recarray
        Record array consisting of given arrayList columns.

    Examples
    --------
    >>> x1=np.array([1,2,3,4])
    >>> x2=np.array(['a','dd','xyz','12'])
    >>> x3=np.array([1.1,2,3,4])
    >>> r = np.rec.fromarrays([x1,x2,x3],names='a,b,c')
    >>> print(r[1])
    (2, 'dd', 2.0) # may vary
    >>> x1[1]=34
    >>> r.a
    array([1, 2, 3, 4])

    >>> x1 = np.array([1, 2, 3, 4])
    >>> x2 = np.array(['a', 'dd', 'xyz', '12'])
    >>> x3 = np.array([1.1, 2, 3,4])
    >>> r = np.rec.fromarrays(
    ...     [x1, x2, x3],
    ...     dtype=np.dtype([('a', np.int32), ('b', 'S3'), ('c', np.float32)]))
    >>> r
    rec.array([(1, b'a', 1.1), (2, b'dd', 2. ), (3, b'xyz', 3. ),
               (4, b'12', 4. )],
              dtype=[('a', '<i4'), ('b', 'S3'), ('c', '<f4')])
    """

    arrayList = [sb.asarray(x) for x in arrayList]

    # NumPy 1.19.0, 2020-01-01
    shape = _deprecate_shape_0_as_None(shape)

    if shape is None:
        shape = arrayList[0].shape
    elif isinstance(shape, int):
        shape = (shape,)

    if formats is None and dtype is None:
        # go through each object in the list to see if it is an ndarray
        # and determine the formats.
        formats = [obj.dtype for obj in arrayList]

    if dtype is not None:
        descr = sb.dtype(dtype)
    else:
        descr = format_parser(formats, names, titles, aligned, byteorder).dtype
    _names = descr.names

    # Determine shape from data-type.
    if len(descr) != len(arrayList):
        raise ValueError("mismatch between the number of fields "
                "and the number of arrays")

    d0 = descr[0].shape
    nn = len(d0)
    if nn > 0:
        shape = shape[:-nn]

    _array = recarray(shape, descr)

    # populate the record array (makes a copy)
    for k, obj in enumerate(arrayList):
        nn = descr[k].ndim
        testshape = obj.shape[:obj.ndim - nn]
        name = _names[k]
        if testshape != shape:
            raise ValueError(f'array-shape mismatch in array {k} ("{name}")')

        _array[name] = obj

    return _array

