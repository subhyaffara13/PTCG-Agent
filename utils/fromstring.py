
def fromstring(text, parser=None, base_url=None, forbid_dtd=False, forbid_entities=True):
    if parser is None:
        parser = getDefaultParser()
    rootelement = _etree.fromstring(text, parser, base_url=base_url)
    elementtree = rootelement.getroottree()
    check_docinfo(elementtree, forbid_dtd, forbid_entities)
    return rootelement


def fromstring(s, language=Language.C):
    """Create an expression from a string.

    This is a "lazy" parser, that is, only arithmetic operations are
    resolved, non-arithmetic operations are treated as symbols.
    """
    r = _FromStringWorker(language=language).parse(s)
    if isinstance(r, Expr):
        return r
    raise ValueError(f'failed to parse `{s}` to Expr instance: got `{r}`')


def fromstring(datastring, dtype=None, shape=None, offset=0, formats=None,
               names=None, titles=None, aligned=False, byteorder=None):
    r"""Create a record array from binary data

    Note that despite the name of this function it does not accept `str`
    instances.

    Parameters
    ----------
    datastring : bytes-like
        Buffer of binary data
    dtype : data-type, optional
        Valid dtype for all arrays
    shape : int or tuple of ints, optional
        Shape of each array.
    offset : int, optional
        Position in the buffer to start reading from.
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation.


    Returns
    -------
    np.recarray
        Record array view into the data in datastring. This will be readonly
        if `datastring` is readonly.

    See Also
    --------
    numpy.frombuffer

    Examples
    --------
    >>> a = b'\x01\x02\x03abc'
    >>> np.rec.fromstring(a, dtype='u1,u1,u1,S3')
    rec.array([(1, 2, 3, b'abc')],
            dtype=[('f0', 'u1'), ('f1', 'u1'), ('f2', 'u1'), ('f3', 'S3')])

    >>> grades_dtype = [('Name', (np.str_, 10)), ('Marks', np.float64),
    ...                 ('GradeLevel', np.int32)]
    >>> grades_array = np.array([('Sam', 33.3, 3), ('Mike', 44.4, 5),
    ...                         ('Aadi', 66.6, 6)], dtype=grades_dtype)
    >>> np.rec.fromstring(grades_array.tobytes(), dtype=grades_dtype)
    rec.array([('Sam', 33.3, 3), ('Mike', 44.4, 5), ('Aadi', 66.6, 6)],
            dtype=[('Name', '<U10'), ('Marks', '<f8'), ('GradeLevel', '<i4')])

    >>> s = '\x01\x02\x03abc'
    >>> np.rec.fromstring(s, dtype='u1,u1,u1,S3')
    Traceback (most recent call last):
       ...
    TypeError: a bytes-like object is required, not 'str'
    """

    if dtype is None and formats is None:
        raise TypeError("fromstring() needs a 'dtype' or 'formats' argument")

    if dtype is not None:
        descr = sb.dtype(dtype)
    else:
        descr = format_parser(formats, names, titles, aligned, byteorder).dtype

    itemsize = descr.itemsize

    # NumPy 1.19.0, 2020-01-01
    shape = _deprecate_shape_0_as_None(shape)

    if shape in (None, -1):
        shape = (len(datastring) - offset) // itemsize

    _array = recarray(shape, descr, buf=datastring, offset=offset)
    return _array


def fromstring(string: str, dtype: DTypeLike = float, count: int = -1, *, sep: str) -> Array:
  """Convert a string of text into 1-D JAX array.

  JAX implementation of :func:`numpy.fromstring`.

  Args:
    string: input string containing the data.
    dtype: optional. Desired data type for the array. Default is ``float``.
    count: optional integer specifying the number of items to read from the string.
      If -1 (default), all items are read.
    sep: the string used to separate values in the input string.

  Returns:
    A 1-D JAX array containing the parsed data from the input string.

  See also:
    - :func:`jax.numpy.frombuffer`: construct a JAX array from an object
      that implements the buffer interface.

  Examples:
    >>> jnp.fromstring("1 2 3", dtype=int, sep=" ")
    Array([1, 2, 3], dtype=int32)
    >>> jnp.fromstring("0.1, 0.2, 0.3", dtype=float, count=2, sep=",")
    Array([0.1, 0.2], dtype=float32)
  """
  return asarray(np.fromstring(string=string, dtype=dtype, count=count, sep=sep))

