
def read_array(fp, allow_pickle=False, pickle_kwargs=None, *,
               max_header_size=_MAX_HEADER_SIZE):
    """
    Read an array from an NPY file.

    Parameters
    ----------
    fp : file_like object
        If this is not a real file object, then this may take extra memory
        and time.
    allow_pickle : bool, optional
        Whether to allow writing pickled data. Default: False
    pickle_kwargs : dict
        Additional keyword arguments to pass to pickle.load. These are only
        useful when loading object arrays saved on Python 2.
    max_header_size : int, optional
        Maximum allowed size of the header.  Large headers may not be safe
        to load securely and thus require explicitly passing a larger value.
        See :py:func:`ast.literal_eval()` for details.
        This option is ignored when `allow_pickle` is passed.  In that case
        the file is by definition trusted and the limit is unnecessary.

    Returns
    -------
    array : ndarray
        The array from the data on disk.

    Raises
    ------
    ValueError
        If the data is invalid, or allow_pickle=False and the file contains
        an object array.

    """
    if allow_pickle:
        # Effectively ignore max_header_size, since `allow_pickle` indicates
        # that the input is fully trusted.
        max_header_size = 2**64

    version = read_magic(fp)
    _check_version(version)
    shape, fortran_order, dtype = _read_array_header(
            fp, version, max_header_size=max_header_size)
    if len(shape) == 0:
        count = 1
    else:
        count = numpy.multiply.reduce(shape, dtype=numpy.int64)

    # Now read the actual data.
    if dtype.hasobject:
        # The array contained Python objects. We need to unpickle the data.
        if not allow_pickle:
            raise ValueError("Object arrays cannot be loaded when "
                             "allow_pickle=False")
        if pickle_kwargs is None:
            pickle_kwargs = {}
        try:
            array = pickle.load(fp, **pickle_kwargs)
        except UnicodeError as err:
            # Friendlier error message
            raise UnicodeError(
                f"Unpickling a python object failed: {err!r}\n"
                "You may need to pass the encoding= option "
                "to numpy.load"
            ) from err
    else:
        if isfileobj(fp):
            # We can use the fast fromfile() function.
            array = numpy.fromfile(fp, dtype=dtype, count=count)
        else:
            # This is not a real file. We have to read it the
            # memory-intensive way.
            # crc32 module fails on reads greater than 2 ** 32 bytes,
            # breaking large reads from gzip streams. Chunk reads to
            # BUFFER_SIZE bytes to avoid issue and reduce memory overhead
            # of the read. In non-chunked case count < max_read_count, so
            # only one read is performed.

            # Use np.ndarray instead of np.empty since the latter does
            # not correctly instantiate zero-width string dtypes; see
            # https://github.com/numpy/numpy/pull/6430
            array = numpy.ndarray(count, dtype=dtype)

            if dtype.itemsize > 0:
                # If dtype.itemsize == 0 then there's nothing more to read
                max_read_count = BUFFER_SIZE // min(BUFFER_SIZE, dtype.itemsize)

                for i in range(0, count, max_read_count):
                    read_count = min(max_read_count, count - i)
                    read_size = int(read_count * dtype.itemsize)
                    data = _read_bytes(fp, read_size, "array data")
                    array[i:i + read_count] = numpy.frombuffer(data, dtype=dtype,
                                                             count=read_count)

        if array.size != count:
            raise ValueError(
                "Failed to read all data for array. "
                f"Expected {shape} = {count} elements, "
                f"could only read {array.size} elements. "
                "(file seems not fully written?)"
            )

        if fortran_order:
            array = array.reshape(shape[::-1])
            array = array.transpose()
        else:
            array = array.reshape(shape)

    return array

