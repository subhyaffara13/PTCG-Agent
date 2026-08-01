
def relabel_result(
    result: DataFrame | Series,
    func: dict[str, list[Callable | str]],
    columns: Iterable[Hashable],
    order: Iterable[int],
) -> dict[Hashable, Series]:
    """
    Internal function to reorder result if relabelling is True for
    dataframe.agg, and return the reordered result in dict.

    Parameters:
    ----------
    result: Result from aggregation
    func: Dict of (column name, funcs)
    columns: New columns name for relabelling
    order: New order for relabelling

    Examples
    --------
    >>> from pandas.core.apply import relabel_result
    >>> result = pd.DataFrame(
    ...     {"A": [np.nan, 2, np.nan], "C": [6, np.nan, np.nan], "B": [np.nan, 4, 2.5]},
    ...     index=["max", "mean", "min"],
    ... )
    >>> funcs = {"A": ["max"], "C": ["max"], "B": ["mean", "min"]}
    >>> columns = ("foo", "aab", "bar", "dat")
    >>> order = [0, 1, 2, 3]
    >>> result_in_dict = relabel_result(result, funcs, columns, order)
    >>> pd.DataFrame(result_in_dict, index=columns)
           A    C    B
    foo  2.0  NaN  NaN
    aab  NaN  6.0  NaN
    bar  NaN  NaN  4.0
    dat  NaN  NaN  2.5
    """
    from pandas.core.indexes.base import Index

    reordered_indexes = [
        pair[0] for pair in sorted(zip(columns, order, strict=True), key=lambda t: t[1])
    ]
    reordered_result_in_dict: dict[Hashable, Series] = {}
    idx = 0

    reorder_mask = not isinstance(result, ABCSeries) and len(result.columns) > 1
    for col, fun in func.items():
        s = result[col].dropna()

        # In the `_aggregate`, the callable names are obtained and used in `result`, and
        # these names are ordered alphabetically. e.g.
        #           C2   C1
        # <lambda>   1  NaN
        # amax     NaN  4.0
        # max      NaN  4.0
        # sum     18.0  6.0
        # Therefore, the order of functions for each column could be shuffled
        # accordingly so need to get the callable name if it is not parsed names, and
        # reorder the aggregated result for each column.
        # e.g. if df.agg(c1=("C2", sum), c2=("C2", lambda x: min(x))), correct order is
        # [sum, <lambda>], but in `result`, it will be [<lambda>, sum], and we need to
        # reorder so that aggregated values map to their functions regarding the order.

        # However there is only one column being used for aggregation, not need to
        # reorder since the index is not sorted, and keep as is in `funcs`, e.g.
        #         A
        # min   1.0
        # mean  1.5
        # mean  1.5
        if reorder_mask:
            fun = [
                com.get_callable_name(f) if not isinstance(f, str) else f for f in fun
            ]
            col_idx_order = Index(s.index, copy=False).get_indexer(fun)
            valid_idx = col_idx_order != -1
            if valid_idx.any():
                s = s.iloc[col_idx_order[valid_idx]]
        # assign the new user-provided "named aggregation" as index names, and reindex
        # it based on the whole user-provided names.
        if not s.empty:
            s.index = reordered_indexes[idx : idx + len(fun)]
        reordered_result_in_dict[col] = s.reindex(columns)
        idx = idx + len(fun)
    return reordered_result_in_dict

