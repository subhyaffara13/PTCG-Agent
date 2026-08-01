
def melt(
    frame: DataFrame,
    id_vars=None,
    value_vars=None,
    var_name=None,
    value_name: Hashable = "value",
    col_level=None,
    ignore_index: bool = True,
) -> DataFrame:
    """
    Unpivot a DataFrame from wide to long format, optionally leaving identifiers set.

    This function is useful to reshape a DataFrame into a format where one
    or more columns are identifier variables (`id_vars`), while all other
    columns are considered measured variables (`value_vars`), and are "unpivoted" to
    the row axis, leaving just two non-identifier columns, 'variable' and
    'value'.

    Parameters
    ----------
    frame : DataFrame
        The DataFrame to unpivot.
    id_vars : scalar, tuple, list, or ndarray, optional
        Column(s) to use as identifier variables.
    value_vars : scalar, tuple, list, or ndarray, optional
        Column(s) to unpivot. If not specified, uses all columns that
        are not set as `id_vars`.
    var_name : scalar, tuple, list, or ndarray, optional
        Name to use for the 'variable' column. If None it uses
        ``frame.columns.name`` or 'variable'. Must be a scalar if columns are a
        MultiIndex.
    value_name : scalar, default 'value'
        Name to use for the 'value' column, can't be an existing column label.
    col_level : scalar, optional
        If columns are a MultiIndex then use this level to melt.
    ignore_index : bool, default True
        If True, original index is ignored. If False, the original index is retained.
        Index labels will be repeated as necessary.

    Returns
    -------
    DataFrame
        Unpivoted DataFrame.

    See Also
    --------
    DataFrame.melt : Identical method.
    pivot_table : Create a spreadsheet-style pivot table as a DataFrame.
    DataFrame.pivot : Return reshaped DataFrame organized
        by given index / column values.
    DataFrame.explode : Explode a DataFrame from list-like
            columns to long format.

    Notes
    -----
    Reference :ref:`the user guide <reshaping.melt>` for more examples.

    Examples
    --------
    >>> df = pd.DataFrame(
    ...     {
    ...         "A": {0: "a", 1: "b", 2: "c"},
    ...         "B": {0: 1, 1: 3, 2: 5},
    ...         "C": {0: 2, 1: 4, 2: 6},
    ...     }
    ... )
    >>> df
    A  B  C
    0  a  1  2
    1  b  3  4
    2  c  5  6

    >>> pd.melt(df, id_vars=["A"], value_vars=["B"])
    A variable  value
    0  a        B      1
    1  b        B      3
    2  c        B      5

    >>> pd.melt(df, id_vars=["A"], value_vars=["B", "C"])
    A variable  value
    0  a        B      1
    1  b        B      3
    2  c        B      5
    3  a        C      2
    4  b        C      4
    5  c        C      6

    The names of 'variable' and 'value' columns can be customized:

    >>> pd.melt(
    ...     df,
    ...     id_vars=["A"],
    ...     value_vars=["B"],
    ...     var_name="myVarname",
    ...     value_name="myValname",
    ... )
    A myVarname  myValname
    0  a         B          1
    1  b         B          3
    2  c         B          5

    Original index values can be kept around:

    >>> pd.melt(df, id_vars=["A"], value_vars=["B", "C"], ignore_index=False)
    A variable  value
    0  a        B      1
    1  b        B      3
    2  c        B      5
    0  a        C      2
    1  b        C      4
    2  c        C      6

    If you have multi-index columns:

    >>> df.columns = [list("ABC"), list("DEF")]
    >>> df
    A  B  C
    D  E  F
    0  a  1  2
    1  b  3  4
    2  c  5  6

    >>> pd.melt(df, col_level=0, id_vars=["A"], value_vars=["B"])
    A variable  value
    0  a        B      1
    1  b        B      3
    2  c        B      5

    >>> pd.melt(df, id_vars=[("A", "D")], value_vars=[("B", "E")])
    (A, D) variable_0 variable_1  value
    0      a          B          E      1
    1      b          B          E      3
    2      c          B          E      5
    """
    if value_name in frame.columns:
        raise ValueError(
            f"value_name ({value_name}) cannot match an element in "
            "the DataFrame columns."
        )
    id_vars = ensure_list_vars(id_vars, "id_vars", frame.columns)
    value_vars_was_not_none = value_vars is not None
    value_vars = ensure_list_vars(value_vars, "value_vars", frame.columns)

    # GH61475 - prevent AttributeError when duplicate column in id_vars
    if len(frame.columns.get_indexer_for(id_vars)) > len(id_vars):
        raise ValueError("id_vars cannot contain duplicate columns.")

    if id_vars or value_vars:
        if col_level is not None:
            level = frame.columns.get_level_values(col_level)
        else:
            level = frame.columns
        labels = id_vars + value_vars
        idx = level.get_indexer_for(labels)
        missing = idx == -1
        if missing.any():
            missing_labels = [
                lab for lab, not_found in zip(labels, missing, strict=True) if not_found
            ]
            raise KeyError(
                "The following id_vars or value_vars are not present in "
                f"the DataFrame: {missing_labels}"
            )
        if value_vars_was_not_none:
            frame = frame.iloc[:, algos.unique(idx)]
        else:
            frame = frame.copy(deep=False)
    else:
        frame = frame.copy(deep=False)

    if col_level is not None:  # allow list or other?
        # frame is a copy
        frame.columns = frame.columns.get_level_values(col_level)

    if var_name is None:
        if isinstance(frame.columns, MultiIndex):
            if len(frame.columns.names) == len(set(frame.columns.names)):
                var_name = frame.columns.names
            else:
                var_name = [f"variable_{i}" for i in range(len(frame.columns.names))]
        else:
            var_name = [
                frame.columns.name if frame.columns.name is not None else "variable"
            ]
    elif is_list_like(var_name):
        if isinstance(frame.columns, MultiIndex):
            if is_iterator(var_name):
                var_name = list(var_name)
            if len(var_name) > len(frame.columns):
                raise ValueError(
                    f"{var_name=} has {len(var_name)} items, "
                    f"but the dataframe columns only have {len(frame.columns)} levels."
                )
        else:
            raise ValueError(f"{var_name=} must be a scalar.")
    else:
        var_name = [var_name]

    num_rows, K = frame.shape
    num_cols_adjusted = K - len(id_vars)

    mdata: dict[Hashable, AnyArrayLike] = {}
    for col in id_vars:
        id_data = frame.pop(col)
        if not isinstance(id_data.dtype, np.dtype):
            # i.e. ExtensionDtype
            if num_cols_adjusted > 0:
                mdata[col] = concat([id_data] * num_cols_adjusted, ignore_index=True)
            else:
                # We can't concat empty list. (GH 46044)
                mdata[col] = type(id_data)([], name=id_data.name, dtype=id_data.dtype)
        else:
            mdata[col] = np.tile(id_data._values, num_cols_adjusted)

    mcolumns = id_vars + var_name + [value_name]

    if frame.shape[1] > 0 and not any(
        not isinstance(dt, np.dtype) and dt._supports_2d for dt in frame.dtypes
    ):
        mdata[value_name] = concat(
            [frame.iloc[:, i] for i in range(frame.shape[1])], ignore_index=True
        ).values
    else:
        mdata[value_name] = frame._values.ravel("F")
    for i, col in enumerate(var_name):
        mdata[col] = frame.columns._get_level_values(i).repeat(num_rows)

    result = frame._constructor(mdata, columns=mcolumns)

    if not ignore_index:
        taker = np.tile(np.arange(len(frame)), num_cols_adjusted)
        result.index = frame.index.take(taker)

    return result

