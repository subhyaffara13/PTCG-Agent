
def fromregex(file, regexp, dtype, encoding=None):
    r"""
    Construct an array from a text file, using regular expression parsing.

    The returned array is always a structured array, and is constructed from
    all matches of the regular expression in the file. Groups in the regular
    expression are converted to fields of the structured array.

    Parameters
    ----------
    file : file, str, or pathlib.Path
        Filename or file object to read.

        .. versionchanged:: 1.22.0
            Now accepts `os.PathLike` implementations.

    regexp : str or regexp
        Regular expression used to parse the file.
        Groups in the regular expression correspond to fields in the dtype.
    dtype : dtype or list of dtypes
        Dtype for the structured array; must be a structured datatype.
    encoding : str, optional
        Encoding used to decode the inputfile. Does not apply to input streams.

    Returns
    -------
    output : ndarray
        The output array, containing the part of the content of `file` that
        was matched by `regexp`. `output` is always a structured array.

    Raises
    ------
    TypeError
        When `dtype` is not a valid dtype for a structured array.

    See Also
    --------
    fromstring, loadtxt

    Notes
    -----
    Dtypes for structured arrays can be specified in several forms, but all
    forms specify at least the data type and field name. For details see
    `basics.rec`.

    Examples
    --------
    >>> import numpy as np
    >>> from io import StringIO
    >>> text = StringIO("1312 foo\n1534  bar\n444   qux")

    >>> regexp = r"(\d+)\s+(...)"  # match [digits, whitespace, anything]
    >>> output = np.fromregex(text, regexp,
    ...                       [('num', np.int64), ('key', 'S3')])
    >>> output
    array([(1312, b'foo'), (1534, b'bar'), ( 444, b'qux')],
          dtype=[('num', '<i8'), ('key', 'S3')])
    >>> output['num']
    array([1312, 1534,  444])

    """
    own_fh = False
    if not hasattr(file, "read"):
        file = os.fspath(file)
        file = np.lib._datasource.open(file, 'rt', encoding=encoding)
        own_fh = True

    try:
        if not isinstance(dtype, np.dtype):
            dtype = np.dtype(dtype)
        if dtype.names is None:
            raise TypeError('dtype must be a structured datatype.')

        content = file.read()
        if isinstance(content, bytes) and isinstance(regexp, str):
            regexp = asbytes(regexp)

        if not hasattr(regexp, 'match'):
            regexp = re.compile(regexp)
        seq = regexp.findall(content)
        if seq and not isinstance(seq[0], tuple):
            # Only one group is in the regexp.
            # Create the new array as a single data-type and then
            #   re-interpret as a single-field structured array.
            newdtype = np.dtype(dtype[dtype.names[0]])
            output = np.array(seq, dtype=newdtype)
            output = output.view(dtype)
        else:
            output = np.array(seq, dtype=dtype)

        return output
    finally:
        if own_fh:
            file.close()

