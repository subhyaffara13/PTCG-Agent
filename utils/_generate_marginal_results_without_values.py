
def _generate_marginal_results_without_values(
    table: DataFrame,
    data: DataFrame,
    rows,
    cols,
    aggfunc,
    kwargs,
    observed: bool,
    margins_name: Hashable = "All",
    dropna: bool = True,
):
    margin_keys: list | Index
    if len(cols) > 0:
        # need to "interleave" the margins
        margin_keys = []

        def _all_key():
            if len(cols) == 1:
                return margins_name
            return (margins_name,) + ("",) * (len(cols) - 1)

        if len(rows) > 0:
            margin = data.groupby(rows, observed=observed, dropna=dropna)[rows].apply(
                aggfunc, **kwargs
            )
            all_key = _all_key()
            table[all_key] = margin
            result = table
            margin_keys.append(all_key)

        else:
            margin = data.groupby(level=0, observed=observed, dropna=dropna).apply(
                aggfunc, **kwargs
            )
            all_key = _all_key()
            table[all_key] = margin
            result = table
            margin_keys.append(all_key)
            return result
    else:
        result = table
        margin_keys = table.columns

    if len(cols):
        row_margin = data.groupby(cols, observed=observed, dropna=dropna)[cols].apply(
            aggfunc, **kwargs
        )
    else:
        row_margin = Series(np.nan, index=result.columns)

    return result, margin_keys, row_margin

