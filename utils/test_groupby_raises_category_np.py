
def test_groupby_raises_category_np(
    how, by, groupby_series, groupby_func_np, df_with_cat_col
):
    # GH#50749
    df = df_with_cat_col
    gb = df.groupby(by=by)

    if groupby_series:
        gb = gb["d"]

    klass, msg = {
        np.sum: (TypeError, "dtype category does not support operation 'sum'"),
        np.mean: (
            TypeError,
            "dtype category does not support operation 'mean'",
        ),
    }[groupby_func_np]
    _call_and_check(klass, msg, how, gb, groupby_func_np, ())

