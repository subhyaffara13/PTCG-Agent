
def test_numeric_only(kernel, has_arg, numeric_only, keys):
    # GH#46072
    # drops_nuisance: Whether the op drops nuisance columns even when numeric_only=False
    # has_arg: Whether the op has a numeric_only arg
    df = DataFrame({"a1": [1, 1], "a2": [2, 2], "a3": [5, 6], "b": 2 * [object]})

    args = get_groupby_method_args(kernel, df)
    kwargs = {} if numeric_only is lib.no_default else {"numeric_only": numeric_only}

    gb = df.groupby(keys)
    method = getattr(gb, kernel)
    if has_arg and numeric_only is True:
        # Cases where b does not appear in the result
        if kernel == "corrwith":
            warn = Pandas4Warning
            msg = "DataFrameGroupBy.corrwith is deprecated"
        else:
            warn = None
            msg = ""
        with tm.assert_produces_warning(warn, match=msg):
            result = method(*args, **kwargs)
        assert "b" not in result.columns
    elif (
        # kernels that work on any dtype and have numeric_only arg
        kernel in ("first", "last")
        or (
            # kernels that work on any dtype and don't have numeric_only arg
            kernel in ("any", "all", "bfill", "ffill", "nth", "nunique")
            and numeric_only is lib.no_default
        )
    ):
        result = method(*args, **kwargs)
        assert "b" in result.columns
    elif has_arg:
        assert numeric_only is not True
        # kernels that are successful on any dtype were above; this will fail

        # object dtypes for transformations are not implemented in Cython and
        # have no Python fallback
        exception = NotImplementedError if kernel.startswith("cum") else TypeError

        msg = "|".join(
            [
                "not allowed for this dtype",
                "cannot be performed against 'object' dtypes",
                "must be a string or a real number",
                "unsupported operand type",
                "function is not implemented for this dtype",
                re.escape(f"agg function failed [how->{kernel},dtype->object]"),
            ]
        )
        if kernel == "quantile":
            msg = "dtype 'object' does not support operation 'quantile'"
        elif kernel == "idxmin":
            msg = "'<' not supported between instances of 'type' and 'type'"
        elif kernel == "idxmax":
            msg = "'>' not supported between instances of 'type' and 'type'"
        with pytest.raises(exception, match=msg):
            if kernel == "corrwith":
                warn = Pandas4Warning
                msg = "DataFrameGroupBy.corrwith is deprecated"
            else:
                warn = None
                msg = ""
            with tm.assert_produces_warning(warn, match=msg):
                method(*args, **kwargs)
    elif not has_arg and numeric_only is not lib.no_default:
        with pytest.raises(
            TypeError, match="got an unexpected keyword argument 'numeric_only'"
        ):
            method(*args, **kwargs)
    else:
        assert kernel in ("diff", "pct_change")
        assert numeric_only is lib.no_default
        # Doesn't have numeric_only argument and fails on nuisance columns
        with pytest.raises(TypeError, match=r"unsupported operand type"):
            method(*args, **kwargs)

