
def cartesian_product_for_groupers(result, args, names, fill_value=np.nan):
    """Reindex to a cartesian production for the groupers,
    preserving the nature (Categorical) of each grouper
    """

    def f(a):
        if isinstance(a, (CategoricalIndex, Categorical)):
            categories = a.categories
            a = Categorical.from_codes(
                np.arange(len(categories)), categories=categories, ordered=a.ordered
            )
        return a

    index = MultiIndex.from_product(map(f, args), names=names)
    if isinstance(fill_value, dict):
        # fill_value is a dict mapping column names to fill values
        # -> reindex column by column (reindex itself does not support this)
        res = {}
        for col in result.columns:
            res[col] = result[col].reindex(index, fill_value=fill_value[col])
        return DataFrame(res, index=index).sort_index()

    return result.reindex(index, fill_value=fill_value).sort_index()

