
def write_array(fp, array, version=None, allow_pickle=True, pickle_kwargs=None):
    """
    Write an array to an NPY file, including a header.

    If the array is neither C-contiguous nor Fortran-contiguous AND the
    file_like object is not a real file object, this function will have to
    copy data in memory.

    Parameters
    ----------
    fp : file_like object
        An open, writable file object, or similar object with a
        ``.write()`` method.
    array : ndarray
        The array to write to disk.
    version : (int, int) or None, optional
        The version number of the format. None means use the oldest
        supported version that is able to store the data.  Default: None
    allow_pickle : bool, optional
        Whether to allow writing pickled data. Default: True
    pickle_kwargs : dict, optional
        Additional keyword arguments to pass to pickle.dump, excluding
        'protocol'. These are only useful when pickling objects in object
        arrays to Python 2 compatible format.

    Raises
    ------
    ValueError
        If the array cannot be persisted. This includes the case of
        allow_pickle=False and array being an object array.
    Various other errors
        If the array contains Python objects as part of its dtype, the
        process of pickling them may raise various errors if the objects
        are not picklable.

    """
    _check_version(version)
    _write_array_header(fp, header_data_from_array_1_0(array), version)

    if array.itemsize == 0:
        buffersize = 0
    else:
        # Set buffer size to 16 MiB to hide the Python loop overhead.
        buffersize = max(16 * 1024 ** 2 // array.itemsize, 1)

    dtype_class = type(array.dtype)

    if array.dtype.hasobject or not dtype_class._legacy:
        # We contain Python objects so we cannot write out the data
        # directly.  Instead, we will pickle it out
        if not allow_pickle:
            if array.dtype.hasobject:
                raise ValueError("Object arrays cannot be saved when "
                                 "allow_pickle=False")
            if not dtype_class._legacy:
                raise ValueError("User-defined dtypes cannot be saved "
                                 "when allow_pickle=False")
        if pickle_kwargs is None:
            pickle_kwargs = {}
        pickle.dump(array, fp, protocol=4, **pickle_kwargs)
    elif array.flags.f_contiguous and not array.flags.c_contiguous:
        if isfileobj(fp):
            array.T.tofile(fp)
        else:
            for chunk in numpy.nditer(
                    array, flags=['external_loop', 'buffered', 'zerosize_ok'],
                    buffersize=buffersize, order='F'):
                fp.write(chunk.tobytes('C'))
    elif isfileobj(fp):
        array.tofile(fp)
    else:
        for chunk in numpy.nditer(
                array, flags=['external_loop', 'buffered', 'zerosize_ok'],
                buffersize=buffersize, order='C'):
            fp.write(chunk.tobytes('C'))

