
def fromfile(file, dtype=float, count=-1, sep=''):
    raise NotImplementedError(
        "fromfile() not yet implemented for a MaskedArray.")


def fromfile(fd, dtype=None, shape=None, offset=0, formats=None,
             names=None, titles=None, aligned=False, byteorder=None):
    """Create an array from binary file data

    Parameters
    ----------
    fd : str or file type
        If file is a string or a path-like object then that file is opened,
        else it is assumed to be a file object. The file object must
        support random access (i.e. it must have tell and seek methods).
    dtype : data-type, optional
        valid dtype for all arrays
    shape : int or tuple of ints, optional
        shape of each array.
    offset : int, optional
        Position in the file to start reading from.
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation

    Returns
    -------
    np.recarray
        record array consisting of data enclosed in file.

    Examples
    --------
    >>> from tempfile import TemporaryFile
    >>> a = np.empty(10,dtype='f8,i4,S5')
    >>> a[5] = (0.5,10,'abcde')
    >>>
    >>> fd=TemporaryFile()
    >>> a = a.view(a.dtype.newbyteorder('<'))
    >>> a.tofile(fd)
    >>>
    >>> _ = fd.seek(0)
    >>> r=np.rec.fromfile(fd, formats='f8,i4,S5', shape=10,
    ... byteorder='<')
    >>> print(r[5])
    (0.5, 10, b'abcde')
    >>> r.shape
    (10,)
    """

    if dtype is None and formats is None:
        raise TypeError("fromfile() needs a 'dtype' or 'formats' argument")

    # NumPy 1.19.0, 2020-01-01
    shape = _deprecate_shape_0_as_None(shape)

    if shape is None:
        shape = (-1,)
    elif isinstance(shape, int):
        shape = (shape,)

    if hasattr(fd, 'readinto'):
        # GH issue 2504. fd supports io.RawIOBase or io.BufferedIOBase
        # interface. Example of fd: gzip, BytesIO, BufferedReader
        # file already opened
        ctx = nullcontext(fd)
    else:
        # open file
        ctx = open(os.fspath(fd), 'rb')

    with ctx as fd:
        if offset > 0:
            fd.seek(offset, 1)
        size = get_remaining_size(fd)

        if dtype is not None:
            descr = sb.dtype(dtype)
        else:
            descr = format_parser(
                formats, names, titles, aligned, byteorder
            ).dtype

        itemsize = descr.itemsize

        shapeprod = sb.array(shape).prod(dtype=nt.intp)
        shapesize = shapeprod * itemsize
        if shapesize < 0:
            shape = list(shape)
            shape[shape.index(-1)] = size // -shapesize
            shape = tuple(shape)
            shapeprod = sb.array(shape).prod(dtype=nt.intp)

        nbytes = shapeprod * itemsize

        if nbytes > size:
            raise ValueError(
                    "Not enough bytes left in file for specified "
                    "shape and type."
                )

        # create the array
        _array = recarray(shape, descr)
        nbytesread = fd.readinto(_array.data)
        if nbytesread != nbytes:
            raise OSError("Didn't read as many bytes as expected")

    return _array


def fromfile(*args, **kwargs):
  """Unimplemented JAX wrapper for jnp.fromfile.

  This function is left deliberately unimplemented because it may be non-pure and thus
  unsafe for use with JIT and other JAX transformations. Consider using
  ``jnp.asarray(np.fromfile(...))`` instead, although care should be taken if ``np.fromfile``
  is used within jax transformations because of its potential side-effect of consuming the
  file object; for more information see `Common Gotchas: Pure Functions
  <https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html#pure-functions>`_.
  """
  raise NotImplementedError(
    "jnp.fromfile() is not implemented because it may be non-pure and thus unsafe for use "
    "with JIT and other JAX transformations. Consider using jnp.asarray(np.fromfile(...)) "
    "instead, although care should be taken if np.fromfile is used within a jax transformations "
    "because of its potential side-effect of consuming the file object; for more information see "
    "https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html#pure-functions")

