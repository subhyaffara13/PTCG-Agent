
def test_groupby_raises_datetime(
    how, by, groupby_series, groupby_func, df_with_datetime_col
):
    df = df_with_datetime_col
    args = get_groupby_method_args(groupby_func, df)
    gb = df.groupby(by=by)

    if groupby_series:
        gb = gb["d"]

        if groupby_func == "corrwith":
            assert not hasattr(gb, "corrwith")
            return

    klass, msg = {
        "all": (TypeError, "'all' with datetime64 dtypes is no longer supported"),
        "any": (TypeError, "'any' with datetime64 dtypes is no longer supported"),
        "bfill": (None, ""),
        "corrwith": (TypeError, "cannot perform __mul__ with this index type"),
        "count": (None, ""),
        "cumcount": (None, ""),
        "cummax": (None, ""),
        "cummin": (None, ""),
        "cumprod": (TypeError, "datetime64 type does not support operation 'cumprod'"),
        "cumsum": (TypeError, "datetime64 type does not support operation 'cumsum'"),
        "diff": (None, ""),
        "ffill": (None, ""),
        "first": (None, ""),
        "idxmax": (None, ""),
        "idxmin": (None, ""),
        "last": (None, ""),
        "max": (None, ""),
        "mean": (None, ""),
        "median": (None, ""),
        "min": (None, ""),
        "ngroup": (None, ""),
        "nunique": (None, ""),
        "pct_change": (TypeError, "cannot perform __truediv__ with this index type"),
        "prod": (TypeError, "datetime64 type does not support operation 'prod'"),
        "quantile": (None, ""),
        "rank": (None, ""),
        "sem": (None, ""),
        "shift": (None, ""),
        "size": (None, ""),
        "skew": (
            TypeError,
            "|".join(
                [
                    r"dtype datetime64\[ns\] does not support operation",
                    "datetime64 type does not support operation 'skew'",
                ]
            ),
        ),
        "kurt": (
            TypeError,
            "|".join(
                [
                    r"dtype datetime64\[ns\] does not support operation",
                    "datetime64 type does not support operation 'kurt'",
                ]
            ),
        ),
        "std": (None, ""),
        "sum": (TypeError, "datetime64 type does not support operation 'sum"),
        "var": (TypeError, "datetime64 type does not support operation 'var'"),
    }[groupby_func]

    if groupby_func == "corrwith":
        warn_category = Pandas4Warning
        warn_msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn_category = None
        warn_msg = ""
    _call_and_check(klass, msg, how, gb, groupby_func, args, warn_category, warn_msg)

