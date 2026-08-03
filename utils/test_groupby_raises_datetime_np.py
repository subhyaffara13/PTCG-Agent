import re

def test_groupby_raises_datetime_np(
    how, by, groupby_series, groupby_func_np, df_with_datetime_col
):
    # GH#50749
    df = df_with_datetime_col
    gb = df.groupby(by=by)

    if groupby_series:
        gb = gb["d"]

    klass, msg = {
        np.sum: (
            TypeError,
            re.escape("datetime64[us] does not support operation 'sum'"),
        ),
        np.mean: (None, ""),
    }[groupby_func_np]
    _call_and_check(klass, msg, how, gb, groupby_func_np, ())

