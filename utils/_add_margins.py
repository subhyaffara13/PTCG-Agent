
def _add_margins(
    table: DataFrame | Series,
    data: DataFrame,
    values,
    rows,
    cols,
    aggfunc,
    kwargs,
    observed: bool,
    margins_name: Hashable = "All",
    fill_value=None,
    dropna: bool = True,
):
    if not isinstance(margins_name, str):
        raise ValueError("margins_name argument must be a string")

    msg = f'Conflicting name "{margins_name}" in margins'
    for level in table.index.names:
        if margins_name in table.index.get_level_values(level):
            raise ValueError(msg)

    grand_margin = _compute_grand_margin(data, values, aggfunc, kwargs, margins_name)

    if table.ndim == 2:
        # i.e. DataFrame
        for level in table.columns.names[1:]:
            if margins_name in table.columns.get_level_values(level):
                raise ValueError(msg)

    key: str | tuple[str, ...]
    if len(rows) > 1:
        key = (margins_name,) + ("",) * (len(rows) - 1)
    else:
        key = margins_name

    if not values and isinstance(table, ABCSeries):
        # If there are no values and the table is a series, then there is only
        # one column in the data. Compute grand margin and return it.
        return table._append_internal(
            table._constructor({key: grand_margin[margins_name]})
        )

    elif values:
        marginal_result_set = _generate_marginal_results(
            table,
            data,
            values,
            rows,
            cols,
            aggfunc,
            kwargs,
            observed,
            margins_name,
            dropna,
        )
        if not isinstance(marginal_result_set, tuple):
            return marginal_result_set
        result, margin_keys, row_margin = marginal_result_set
    else:
        # no values, and table is a DataFrame
        assert isinstance(table, ABCDataFrame)
        marginal_result_set = _generate_marginal_results_without_values(
            table, data, rows, cols, aggfunc, kwargs, observed, margins_name, dropna
        )
        if not isinstance(marginal_result_set, tuple):
            return marginal_result_set
        result, margin_keys, row_margin = marginal_result_set

    row_margin = row_margin.reindex(result.columns, fill_value=fill_value)
    # populate grand margin
    for k in margin_keys:
        if isinstance(k, str):
            row_margin[k] = grand_margin[k]
        else:
            row_margin[k] = grand_margin[k[0]]

    from pandas import DataFrame

    margin_dummy = DataFrame(row_margin, columns=Index([key])).T

    row_names = result.index.names
    # check the result column and leave floats

    for dtype in set(result.dtypes):
        if isinstance(dtype, ExtensionDtype):
            # Can hold NA already
            continue

        cols = result.select_dtypes([dtype]).columns
        margin_dummy[cols] = margin_dummy[cols].apply(
            maybe_downcast_to_dtype, args=(dtype,)
        )
    result = concat([result, margin_dummy])
    result.index.names = row_names

    return result

