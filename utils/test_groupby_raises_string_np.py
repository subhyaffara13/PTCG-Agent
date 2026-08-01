
def test_groupby_raises_string_np(
    how,
    by,
    groupby_series,
    groupby_func_np,
    df_with_string_col,
    using_infer_string,
):
    # GH#50749
    df = df_with_string_col
    gb = df.groupby(by=by)

    if groupby_series:
        gb = gb["d"]

    klass, msg = {
        np.sum: (None, ""),
        np.mean: (
            TypeError,
            "Could not convert string .* to numeric|"
            "Cannot perform reduction 'mean' with string dtype",
        ),
    }[groupby_func_np]

    if using_infer_string:
        if groupby_func_np is np.mean:
            klass = TypeError
        msg = f"Cannot perform reduction '{groupby_func_np.__name__}' with string dtype"

    _call_and_check(klass, msg, how, gb, groupby_func_np, ())

