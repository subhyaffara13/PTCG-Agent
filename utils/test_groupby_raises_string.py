import re

def test_groupby_raises_string(
    how, by, groupby_series, groupby_func, df_with_string_col, using_infer_string
):
    df = df_with_string_col
    args = get_groupby_method_args(groupby_func, df)
    gb = df.groupby(by=by)

    if groupby_series:
        gb = gb["d"]

        if groupby_func == "corrwith":
            assert not hasattr(gb, "corrwith")
            return

    klass, msg = {
        "all": (None, ""),
        "any": (None, ""),
        "bfill": (None, ""),
        "corrwith": (TypeError, "Could not convert"),
        "count": (None, ""),
        "cumcount": (None, ""),
        "cummax": (
            (NotImplementedError, TypeError),
            "(function|cummax) is not (implemented|supported) for (this|object) dtype",
        ),
        "cummin": (
            (NotImplementedError, TypeError),
            "(function|cummin) is not (implemented|supported) for (this|object) dtype",
        ),
        "cumprod": (
            (NotImplementedError, TypeError),
            "(function|cumprod) is not (implemented|supported) for (this|object) dtype",
        ),
        "cumsum": (
            (NotImplementedError, TypeError),
            "(function|cumsum) is not (implemented|supported) for (this|object) dtype",
        ),
        "diff": (TypeError, "unsupported operand type"),
        "ffill": (None, ""),
        "first": (None, ""),
        "idxmax": (None, ""),
        "idxmin": (None, ""),
        "last": (None, ""),
        "max": (None, ""),
        "mean": (
            TypeError,
            re.escape("agg function failed [how->mean,dtype->object]"),
        ),
        "median": (
            TypeError,
            re.escape("agg function failed [how->median,dtype->object]"),
        ),
        "min": (None, ""),
        "ngroup": (None, ""),
        "nunique": (None, ""),
        "pct_change": (TypeError, "unsupported operand type"),
        "prod": (
            TypeError,
            re.escape("agg function failed [how->prod,dtype->object]"),
        ),
        "quantile": (TypeError, "dtype 'object' does not support operation 'quantile'"),
        "rank": (None, ""),
        "sem": (ValueError, "could not convert string to float"),
        "shift": (None, ""),
        "size": (None, ""),
        "skew": (ValueError, "could not convert string to float"),
        "kurt": (ValueError, "could not convert string to float"),
        "std": (ValueError, "could not convert string to float"),
        "sum": (None, ""),
        "var": (
            TypeError,
            re.escape("agg function failed [how->var,dtype->"),
        ),
    }[groupby_func]

    if using_infer_string:
        if groupby_func in [
            "prod",
            "mean",
            "median",
            "cumsum",
            "cumprod",
            "std",
            "sem",
            "var",
            "skew",
            "kurt",
            "quantile",
        ]:
            msg = f"dtype 'str' does not support operation '{groupby_func}'"
            if groupby_func in ["sem", "std", "skew", "kurt"]:
                # The object-dtype raises ValueError when trying to convert to numeric.
                klass = TypeError
        elif groupby_func == "pct_change" and df["d"].dtype.storage == "pyarrow":
            # This doesn't go through EA._groupby_op so the message isn't controlled
            #  there.
            msg = "operation 'truediv' not supported for dtype 'str' with dtype 'str'"
        elif groupby_func == "diff" and df["d"].dtype.storage == "pyarrow":
            # This doesn't go through EA._groupby_op so the message isn't controlled
            #  there.
            msg = "operation 'sub' not supported for dtype 'str' with dtype 'str'"

        elif groupby_func in ["cummin", "cummax"]:
            msg = msg.replace("object", "str")
        elif groupby_func == "corrwith":
            msg = "Cannot perform reduction 'mean' with string dtype"

    if groupby_func == "corrwith":
        warn_category = Pandas4Warning
        warn_msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn_category = None
        warn_msg = ""
    _call_and_check(klass, msg, how, gb, groupby_func, args, warn_category, warn_msg)

