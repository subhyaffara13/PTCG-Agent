
def crosstab(*args, levels=None, sparse=False):
    """
    Return table of counts for each possible unique combination in ``*args``.

    When ``len(args) > 1``, the array computed by this function is
    often referred to as a *contingency table* [1]_.

    The arguments must be sequences with the same length.  The second return
    value, `count`, is an integer array with ``len(args)`` dimensions.  If
    `levels` is None, the shape of `count` is ``(n0, n1, ...)``, where ``nk``
    is the number of unique elements in ``args[k]``.

    Parameters
    ----------
    *args : sequences
        A sequence of sequences whose unique aligned elements are to be
        counted.  The sequences in args must all be the same length.
    levels : sequence, optional
        If `levels` is given, it must be a sequence that is the same length as
        `args`.  Each element in `levels` is either a sequence or None.  If it
        is a sequence, it gives the values in the corresponding sequence in
        `args` that are to be counted.  If any value in the sequences in `args`
        does not occur in the corresponding sequence in `levels`, that value
        is ignored and not counted in the returned array `count`.  The default
        value of `levels` for ``args[i]`` is ``np.unique(args[i])``
    sparse : bool, optional
        If True, return a sparse array.  The array will be an instance of
        the `scipy.sparse.coo_array` class.
        Default is False.

    Returns
    -------
    res : CrosstabResult
        An object containing the following attributes:

        elements : tuple of numpy.ndarrays.
            Tuple of length ``len(args)`` containing the arrays of elements
            that are counted in `count`.  These can be interpreted as the
            labels of the corresponding dimensions of `count`. If `levels` was
            given, then if ``levels[i]`` is not None, ``elements[i]`` will
            hold the values given in ``levels[i]``.
        count : numpy.ndarray or scipy.sparse.coo_array
            Counts of the unique elements in ``zip(*args)``, stored in an
            array. Also known as a *contingency table* when ``len(args) > 1``.

    See Also
    --------
    numpy.unique

    Notes
    -----
    .. versionadded:: 1.7.0

    References
    ----------
    .. [1] "Contingency table", http://en.wikipedia.org/wiki/Contingency_table

    Examples
    --------
    >>> from scipy.stats.contingency import crosstab

    Given the lists `a` and `x`, create a contingency table that counts the
    frequencies of the corresponding pairs.

    >>> a = ['A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B']
    >>> x = ['X', 'X', 'X', 'Y', 'Z', 'Z', 'Y', 'Y', 'Z', 'Z']
    >>> res = crosstab(a, x)
    >>> avals, xvals = res.elements
    >>> avals
    array(['A', 'B'], dtype='<U1')
    >>> xvals
    array(['X', 'Y', 'Z'], dtype='<U1')
    >>> res.count
    array([[2, 3, 0],
           [1, 0, 4]])

    So ``('A', 'X')`` occurs twice, ``('A', 'Y')`` occurs three times, etc.

    Higher dimensional contingency tables can be created.

    >>> p = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
    >>> res = crosstab(a, x, p)
    >>> res.count
    array([[[2, 0],
            [2, 1],
            [0, 0]],
           [[1, 0],
            [0, 0],
            [1, 3]]])
    >>> res.count.shape
    (2, 3, 2)

    The values to be counted can be set by using the `levels` argument.
    It allows the elements of interest in each input sequence to be
    given explicitly instead finding the unique elements of the sequence.

    For example, suppose one of the arguments is an array containing the
    answers to a survey question, with integer values 1 to 4.  Even if the
    value 1 does not occur in the data, we want an entry for it in the table.

    >>> q1 = [2, 3, 3, 2, 4, 4, 2, 3, 4, 4, 4, 3, 3, 3, 4]  # 1 does not occur.
    >>> q2 = [4, 4, 2, 2, 2, 4, 1, 1, 2, 2, 4, 2, 2, 2, 4]  # 3 does not occur.
    >>> options = [1, 2, 3, 4]
    >>> res = crosstab(q1, q2, levels=(options, options))
    >>> res.count
    array([[0, 0, 0, 0],
           [1, 1, 0, 1],
           [1, 4, 0, 1],
           [0, 3, 0, 3]])

    If `levels` is given, but an element of `levels` is None, the unique values
    of the corresponding argument are used. For example,

    >>> res = crosstab(q1, q2, levels=(None, options))
    >>> res.elements
    [array([2, 3, 4]), [1, 2, 3, 4]]
    >>> res.count
    array([[1, 1, 0, 1],
           [1, 4, 0, 1],
           [0, 3, 0, 3]])

    If we want to ignore the pairs where 4 occurs in ``q2``, we can
    give just the values [1, 2] to `levels`, and the 4 will be ignored:

    >>> res = crosstab(q1, q2, levels=(None, [1, 2]))
    >>> res.elements
    [array([2, 3, 4]), [1, 2]]
    >>> res.count
    array([[1, 1],
           [1, 4],
           [0, 3]])

    Finally, let's repeat the first example, but return a sparse array:

    >>> res = crosstab(a, x, sparse=True)
    >>> res.count
    <COOrdinate sparse array of dtype 'int64'
        with 4 stored elements and shape (2, 3)>
    >>> res.count.toarray()
    array([[2, 3, 0],
           [1, 0, 4]])

    """
    nargs = len(args)
    if nargs == 0:
        raise TypeError("At least one input sequence is required.")

    len0 = len(args[0])
    if not all(len(a) == len0 for a in args[1:]):
        raise ValueError("All input sequences must have the same length.")

    if levels is None:
        # Call np.unique with return_inverse=True on each argument.
        actual_levels, indices = zip(*[np.unique(a, return_inverse=True)
                                       for a in args])
    else:
        # `levels` is not None...
        if len(levels) != nargs:
            raise ValueError('len(levels) must equal the number of input '
                             'sequences')

        args = [np.asarray(arg) for arg in args]
        mask = np.zeros((nargs, len0), dtype=np.bool_)
        inv = np.zeros((nargs, len0), dtype=np.intp)
        actual_levels = []
        for k, (levels_list, arg) in enumerate(zip(levels, args)):
            if levels_list is None:
                levels_list, inv[k, :] = np.unique(arg, return_inverse=True)
                mask[k, :] = True
            else:
                q = arg == np.asarray(levels_list).reshape(-1, 1)
                mask[k, :] = np.any(q, axis=0)
                qnz = q.T.nonzero()
                inv[k, qnz[0]] = qnz[1]
            actual_levels.append(levels_list)

        mask_all = mask.all(axis=0)
        indices = tuple(inv[:, mask_all])

    if sparse:
        count = coo_array((np.ones(len(indices[0]), dtype=int), indices))
        count.sum_duplicates()
    else:
        shape = [len(u) for u in actual_levels]
        count = np.zeros(shape, dtype=int)
        np.add.at(count, indices, 1)

    return CrosstabResult(actual_levels, count)


def crosstab(
    index,
    columns,
    values=None,
    rownames=None,
    colnames=None,
    aggfunc=None,
    margins: bool = False,
    margins_name: Hashable = "All",
    dropna: bool = True,
    normalize: bool | Literal[0, 1, "all", "index", "columns"] = False,
) -> DataFrame:
    """
    Compute a simple cross tabulation of two (or more) factors.

    By default, computes a frequency table of the factors unless an
    array of values and an aggregation function are passed.

    Parameters
    ----------
    index : array-like, Series, or list of arrays/Series
        Values to group by in the rows.
    columns : array-like, Series, or list of arrays/Series
        Values to group by in the columns.
    values : array-like, optional
        Array of values to aggregate according to the factors.
        Requires `aggfunc` be specified.
    rownames : sequence, default None
        If passed, must match number of row arrays passed.
    colnames : sequence, default None
        If passed, must match number of column arrays passed.
    aggfunc : function, optional
        If specified, requires `values` be specified as well.
    margins : bool, default False
        Add row/column margins (subtotals).
    margins_name : str, default 'All'
        Name of the row/column that will contain the totals
        when margins is True.
    dropna : bool, default True
        Do not include columns whose entries are all NaN.
    normalize : bool, {'all', 'index', 'columns'}, or {0,1}, default False
        Normalize by dividing all values by the sum of values.

        - If passed 'all' or `True`, will normalize over all values.
        - If passed 'index' will normalize over each row.
        - If passed 'columns' will normalize over each column.
        - If margins is `True`, will also normalize margin values.

    Returns
    -------
    DataFrame
        Cross tabulation of the data.

    See Also
    --------
    DataFrame.pivot : Reshape data based on column values.
    pivot_table : Create a pivot table as a DataFrame.

    Notes
    -----
    Any Series passed will have their name attributes used unless row or column
    names for the cross-tabulation are specified.

    Any input passed containing Categorical data will have **all** of its
    categories included in the cross-tabulation, even if the actual data does
    not contain any instances of a particular category.

    In the event that there aren't overlapping indexes an empty DataFrame will
    be returned.

    Reference :ref:`the user guide <reshaping.crosstabulations>` for more examples.

    Examples
    --------
    >>> a = np.array(
    ...     [
    ...         "foo",
    ...         "foo",
    ...         "foo",
    ...         "foo",
    ...         "bar",
    ...         "bar",
    ...         "bar",
    ...         "bar",
    ...         "foo",
    ...         "foo",
    ...         "foo",
    ...     ],
    ...     dtype=object,
    ... )
    >>> b = np.array(
    ...     [
    ...         "one",
    ...         "one",
    ...         "one",
    ...         "two",
    ...         "one",
    ...         "one",
    ...         "one",
    ...         "two",
    ...         "two",
    ...         "two",
    ...         "one",
    ...     ],
    ...     dtype=object,
    ... )
    >>> c = np.array(
    ...     [
    ...         "dull",
    ...         "dull",
    ...         "shiny",
    ...         "dull",
    ...         "dull",
    ...         "shiny",
    ...         "shiny",
    ...         "dull",
    ...         "shiny",
    ...         "shiny",
    ...         "shiny",
    ...     ],
    ...     dtype=object,
    ... )
    >>> pd.crosstab(a, [b, c], rownames=["a"], colnames=["b", "c"])
    b   one        two
    c   dull shiny dull shiny
    a
    bar    1     2    1     0
    foo    2     2    1     2

    Here 'c' and 'f' are not represented in the data and will not be
    shown in the output because dropna is True by default. Set
    dropna=False to preserve categories with no data.

    >>> foo = pd.Categorical(["a", "b"], categories=["a", "b", "c"])
    >>> bar = pd.Categorical(["d", "e"], categories=["d", "e", "f"])
    >>> pd.crosstab(foo, bar)
    col_0  d  e
    row_0
    a      1  0
    b      0  1
    >>> pd.crosstab(foo, bar, dropna=False)
    col_0  d  e  f
    row_0
    a      1  0  0
    b      0  1  0
    c      0  0  0
    """
    if values is None and aggfunc is not None:
        raise ValueError("aggfunc cannot be used without values.")

    if values is not None and aggfunc is None:
        raise ValueError("values cannot be used without an aggfunc.")

    if not is_nested_list_like(index):
        index = [index]
    if not is_nested_list_like(columns):
        columns = [columns]

    common_idx = None
    pass_objs = [x for x in index + columns if isinstance(x, (ABCSeries, ABCDataFrame))]
    if pass_objs:
        common_idx = get_objs_combined_axis(pass_objs, intersect=True, sort=False)

    rownames = _get_names(index, rownames, prefix="row")
    colnames = _get_names(columns, colnames, prefix="col")

    # duplicate names mapped to unique names for pivot op
    (
        rownames_mapper,
        unique_rownames,
        colnames_mapper,
        unique_colnames,
    ) = _build_names_mapper(rownames, colnames)

    from pandas import DataFrame

    data = {
        **dict(zip(unique_rownames, index, strict=True)),
        **dict(zip(unique_colnames, columns, strict=True)),
    }
    df = DataFrame(data, index=common_idx)

    if values is None:
        df["__dummy__"] = 0
        kwargs = {"aggfunc": len, "fill_value": 0}
    else:
        df["__dummy__"] = values
        kwargs = {"aggfunc": aggfunc}

    # error: Argument 7 to "pivot_table" of "DataFrame" has incompatible type
    # "**Dict[str, object]"; expected "Union[...]"
    table = df.pivot_table(
        "__dummy__",
        index=unique_rownames,
        columns=unique_colnames,
        margins=margins,
        margins_name=margins_name,
        dropna=dropna,
        observed=dropna,
        **kwargs,  # type: ignore[arg-type]
    )

    # Post-process
    if normalize is not False:
        table = _normalize(
            table, normalize=normalize, margins=margins, margins_name=margins_name
        )

    table = table.rename_axis(index=rownames_mapper, axis=0)
    table = table.rename_axis(columns=colnames_mapper, axis=1)

    return table

