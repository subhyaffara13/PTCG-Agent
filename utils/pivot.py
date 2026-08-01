
def pivot(M, i, j):
    '''
    M is a matrix, and M[i, j] specifies the pivot element.

    All elements below M[i, j], in the j-th column, will
    be zeroed, if they are not already 0, according to
    Dodgson-Bareiss' integer preserving transformations.

    References
    ==========
    1. Akritas, A. G.: ``A new method for computing polynomial greatest
    common divisors and polynomial remainder sequences.''
    Numerische MatheMatik 52, 119-127, 1988.

    2. Akritas, A. G., G.I. Malaschonok and P.S. Vigklas: ``On a Theorem
    by Van Vleck Regarding Sturm Sequences.''
    Serdica Journal of Computing, 7, No 4, 101-134, 2013.

    '''
    ma = M[:, :] # copy of matrix M
    rs = ma.rows # No. of rows
    cs = ma.cols # No. of cols
    for r in range(i+1, rs):
        if ma[r, j] != 0:
            for c in range(j + 1, cs):
                ma[r, c] = ma[i, j] * ma[r, c] - ma[i, c] * ma[r, j]
            ma[r, j] = 0
    return ma


def pivot(
    data: DataFrame,
    *,
    columns: IndexLabel,
    index: IndexLabel | lib.NoDefault = lib.no_default,
    values: IndexLabel | lib.NoDefault = lib.no_default,
) -> DataFrame:
    """
    Return reshaped DataFrame organized by given index / column values.

    Reshape data (produce a "pivot" table) based on column values. Uses
    unique values from specified `index` / `columns` to form axes of the
    resulting DataFrame. This function does not support data
    aggregation, multiple values will result in a MultiIndex in the
    columns. See the :ref:`User Guide <reshaping>` for more on reshaping.

    Parameters
    ----------
    data : DataFrame
        Input pandas DataFrame object.
    columns : Hashable or a sequence of the previous
        Column to use to make new frame's columns.
    index : Hashable or a sequence of the previous, optional
        Column to use to make new frame's index. If not given, uses existing index.
    values : Hashable or a sequence of the previous, optional
        Column(s) to use for populating new frame's values. If not
        specified, all remaining columns will be used and the result will
        have hierarchically indexed columns.

    Returns
    -------
    DataFrame
        Returns reshaped DataFrame.

    Raises
    ------
    ValueError:
        When there are any `index`, `columns` combinations with multiple
        values. `DataFrame.pivot_table` when you need to aggregate.

    See Also
    --------
    DataFrame.pivot_table : Generalization of pivot that can handle
        duplicate values for one index/column pair.
    DataFrame.unstack : Pivot based on the index values instead of a
        column.
    wide_to_long : Wide panel to long format. Less flexible but more
        user-friendly than melt.

    Notes
    -----
    For finer-tuned control, see hierarchical indexing documentation along
    with the related stack/unstack methods.

    Reference :ref:`the user guide <reshaping.pivot>` for more examples.

    Examples
    --------
    >>> df = pd.DataFrame(
    ...     {
    ...         "foo": ["one", "one", "one", "two", "two", "two"],
    ...         "bar": ["A", "B", "C", "A", "B", "C"],
    ...         "baz": [1, 2, 3, 4, 5, 6],
    ...         "zoo": ["x", "y", "z", "q", "w", "t"],
    ...     }
    ... )
    >>> df
        foo   bar  baz  zoo
    0   one   A    1    x
    1   one   B    2    y
    2   one   C    3    z
    3   two   A    4    q
    4   two   B    5    w
    5   two   C    6    t

    >>> df.pivot(index="foo", columns="bar", values="baz")
    bar  A   B   C
    foo
    one  1   2   3
    two  4   5   6

    >>> df.pivot(index="foo", columns="bar")["baz"]
    bar  A   B   C
    foo
    one  1   2   3
    two  4   5   6

    >>> df.pivot(index="foo", columns="bar", values=["baz", "zoo"])
          baz       zoo
    bar   A  B  C   A  B  C
    foo
    one   1  2  3   x  y  z
    two   4  5  6   q  w  t

    You could also assign a list of column names or a list of index names.

    >>> df = pd.DataFrame(
    ...     {
    ...         "lev1": [1, 1, 1, 2, 2, 2],
    ...         "lev2": [1, 1, 2, 1, 1, 2],
    ...         "lev3": [1, 2, 1, 2, 1, 2],
    ...         "lev4": [1, 2, 3, 4, 5, 6],
    ...         "values": [0, 1, 2, 3, 4, 5],
    ...     }
    ... )
    >>> df
        lev1 lev2 lev3 lev4 values
    0   1    1    1    1    0
    1   1    1    2    2    1
    2   1    2    1    3    2
    3   2    1    2    4    3
    4   2    1    1    5    4
    5   2    2    2    6    5

    >>> df.pivot(index="lev1", columns=["lev2", "lev3"], values="values")
    lev2    1         2
    lev3    1    2    1    2
    lev1
    1     0.0  1.0  2.0  NaN
    2     4.0  3.0  NaN  5.0

    >>> df.pivot(index=["lev1", "lev2"], columns=["lev3"], values="values")
          lev3    1    2
    lev1  lev2
       1     1  0.0  1.0
             2  2.0  NaN
       2     1  4.0  3.0
             2  NaN  5.0

    A ValueError is raised if there are any duplicates.

    >>> df = pd.DataFrame(
    ...     {
    ...         "foo": ["one", "one", "two", "two"],
    ...         "bar": ["A", "A", "B", "C"],
    ...         "baz": [1, 2, 3, 4],
    ...     }
    ... )
    >>> df
       foo bar  baz
    0  one   A    1
    1  one   A    2
    2  two   B    3
    3  two   C    4

    Notice that the first two rows are the same for our `index`
    and `columns` arguments.

    >>> df.pivot(index="foo", columns="bar", values="baz")
    Traceback (most recent call last):
       ...
    ValueError: Index contains duplicate entries, cannot reshape
    """
    columns_listlike = com.convert_to_list_like(columns)

    # If columns is None we will create a MultiIndex level with None as name
    # which might cause duplicated names because None is the default for
    # level names
    if any(name is None for name in data.index.names):
        data = data.copy(deep=False)
        data.index.names = [
            name if name is not None else lib.no_default for name in data.index.names
        ]

    indexed: DataFrame | Series
    if values is lib.no_default:
        if index is not lib.no_default:
            cols = com.convert_to_list_like(index)
        else:
            cols = []

        append = index is lib.no_default
        # error: Unsupported operand types for + ("List[Any]" and "ExtensionArray")
        # error: Unsupported left operand type for + ("ExtensionArray")
        indexed = data.set_index(
            cols + columns_listlike,  # type: ignore[operator]
            append=append,
        )
    else:
        index_list: list[Index] | list[Series]
        if index is lib.no_default:
            if isinstance(data.index, MultiIndex):
                # GH 23955
                index_list = [
                    data.index.get_level_values(i) for i in range(data.index.nlevels)
                ]
            else:
                index_list = [
                    data._constructor_sliced(data.index, name=data.index.name)
                ]
        else:
            index_list = [data[idx] for idx in com.convert_to_list_like(index)]

        data_columns = [data[col] for col in columns_listlike]
        index_list.extend(data_columns)
        multiindex = MultiIndex.from_arrays(index_list)

        if is_list_like(values) and not isinstance(values, tuple):
            # Exclude tuple because it is seen as a single column name
            indexed = data._constructor(
                data[values]._values,
                index=multiindex,
                columns=cast("SequenceNotStr", values),
            )
        else:
            indexed = data._constructor_sliced(data[values]._values, index=multiindex)
    # error: Argument 1 to "unstack" of "DataFrame" has incompatible type "Union
    # [List[Any], ExtensionArray, ndarray[Any, Any], Index, Series]"; expected
    # "Hashable"
    # unstack with a MultiIndex returns a DataFrame
    result = cast("DataFrame", indexed.unstack(columns_listlike))  # type: ignore[arg-type]
    result.index.names = [
        name if name is not lib.no_default else None for name in result.index.names
    ]

    return result

