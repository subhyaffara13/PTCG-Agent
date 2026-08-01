
def get_dummies(
    data,
    prefix=None,
    prefix_sep: str | Iterable[str] | dict[str, str] = "_",
    dummy_na: bool = False,
    columns=None,
    sparse: bool = False,
    drop_first: bool = False,
    dtype: NpDtype | None = None,
) -> DataFrame:
    """
    Convert categorical variable into dummy/indicator variables.

    Each variable is converted in as many 0/1 variables as there are different
    values. Columns in the output are each named after a value; if the input is
    a DataFrame, the name of the original variable is prepended to the value.

    Parameters
    ----------
    data : array-like, Series, or DataFrame
        Data of which to get dummy indicators.
    prefix : str, list of str, or dict of str, default None
        A string to be prepended to DataFrame column names.
        Pass a list with length equal to the number of columns
        when calling get_dummies on a DataFrame. Alternatively, `prefix`
        can be a dictionary mapping column names to prefixes.
    prefix_sep : str, list of str, or dict of str, default '_'
        Should you choose to prepend DataFrame column names with a prefix, this
        is the separator/delimiter to use between the two. Alternatively,
        `prefix_sep` can be a list with length equal to the number of columns,
        or a dictionary mapping column names to separators.
    dummy_na : bool, default False
        If True, a NaN indicator column will be added even if no NaN values are present.
        If False, NA values are encoded as all zero.
    columns : list-like, default None
        Column names in the DataFrame to be encoded.
        If `columns` is None then all the columns with
        `object`, `string`, or `category` dtype will be converted.
    sparse : bool, default False
        Whether the dummy-encoded columns should be backed by
        a :class:`SparseArray` (True) or a regular NumPy array (False).
    drop_first : bool, default False
        Whether to get k-1 dummies out of k categorical levels by removing the
        first level.
    dtype : dtype, default bool
        Data type for new columns. Only a single dtype is allowed.

    Returns
    -------
    DataFrame
        Dummy-coded data. If `data` contains other columns than the
        dummy-coded one(s), these will be prepended, unaltered, to the result.

    See Also
    --------
    Series.str.get_dummies : Convert Series of strings to dummy codes.
    :func:`~pandas.from_dummies` : Convert dummy codes to categorical ``DataFrame``.

    Notes
    -----
    Reference :ref:`the user guide <reshaping.dummies>` for more examples.

    Examples
    --------
    >>> s = pd.Series(list("abca"))

    >>> pd.get_dummies(s)
           a      b      c
    0   True  False  False
    1  False   True  False
    2  False  False   True
    3   True  False  False

    >>> s1 = ["a", "b", np.nan]

    >>> pd.get_dummies(s1)
           a      b
    0   True  False
    1  False   True
    2  False  False

    >>> pd.get_dummies(s1, dummy_na=True)
           a      b    NaN
    0   True  False  False
    1  False   True  False
    2  False  False   True

    >>> df = pd.DataFrame({"A": ["a", "b", "a"], "B": ["b", "a", "c"], "C": [1, 2, 3]})

    >>> pd.get_dummies(df, prefix=["col1", "col2"])
       C  col1_a  col1_b  col2_a  col2_b  col2_c
    0  1    True   False   False    True   False
    1  2   False    True    True   False   False
    2  3    True   False   False   False    True

    >>> pd.get_dummies(pd.Series(list("abcaa")))
           a      b      c
    0   True  False  False
    1  False   True  False
    2  False  False   True
    3   True  False  False
    4   True  False  False

    >>> pd.get_dummies(pd.Series(list("abcaa")), drop_first=True)
           b      c
    0  False  False
    1   True  False
    2  False   True
    3  False  False
    4  False  False

    >>> pd.get_dummies(pd.Series(list("abc")), dtype=float)
         a    b    c
    0  1.0  0.0  0.0
    1  0.0  1.0  0.0
    2  0.0  0.0  1.0
    """
    from pandas.core.reshape.concat import concat

    dtypes_to_encode = ["object", "string", "category"]

    if isinstance(data, DataFrame):
        # determine columns being encoded
        if columns is None:
            data_to_encode = data.select_dtypes(include=dtypes_to_encode)
        elif not is_list_like(columns):
            raise TypeError("Input must be a list-like for parameter `columns`")
        else:
            data_to_encode = data[columns]

        # validate prefixes and separator to avoid silently dropping cols
        def check_len(item, name: str) -> None:
            if is_list_like(item):
                if not len(item) == data_to_encode.shape[1]:
                    len_msg = (
                        f"Length of '{name}' ({len(item)}) did not match the "
                        "length of the columns being encoded "
                        f"({data_to_encode.shape[1]})."
                    )
                    raise ValueError(len_msg)

        check_len(prefix, "prefix")
        check_len(prefix_sep, "prefix_sep")

        if isinstance(prefix, str):
            prefix = itertools.repeat(prefix, len(data_to_encode.columns))
        if isinstance(prefix, dict):
            prefix = [prefix[col] for col in data_to_encode.columns]

        if prefix is None:
            prefix = data_to_encode.columns

        # validate separators
        if isinstance(prefix_sep, str):
            prefix_sep = itertools.repeat(prefix_sep, len(data_to_encode.columns))
        elif isinstance(prefix_sep, dict):
            prefix_sep = [prefix_sep[col] for col in data_to_encode.columns]

        with_dummies: list[DataFrame]
        if data_to_encode.shape == data.shape:
            # Encoding the entire df, do not prepend any dropped columns
            with_dummies = []
        elif columns is not None:
            # Encoding only cols specified in columns. Get all cols not in
            # columns to prepend to result.
            with_dummies = [data.drop(columns, axis=1)]
        else:
            # Encoding only object and category dtype columns. Get remaining
            # columns to prepend to result.
            with_dummies = [data.select_dtypes(exclude=dtypes_to_encode)]

        for col, pre, sep in zip(
            data_to_encode.items(), prefix, prefix_sep, strict=True
        ):
            # col is (column_name, column), use just column data here
            dummy = _get_dummies_1d(
                col[1],
                prefix=pre,
                prefix_sep=sep,
                dummy_na=dummy_na,
                sparse=sparse,
                drop_first=drop_first,
                dtype=dtype,
            )
            with_dummies.append(dummy)
        result = concat(with_dummies, axis=1)
    else:
        result = _get_dummies_1d(
            data,
            prefix,
            prefix_sep,
            dummy_na,
            sparse=sparse,
            drop_first=drop_first,
            dtype=dtype,
        )
    return result

