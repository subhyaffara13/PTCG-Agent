import re

def test_omit_nuisance_agg(df, agg_function, numeric_only, using_infer_string):
    # GH 38774, GH 38815
    grouped = df.groupby("A")

    no_drop_nuisance = ("var", "std", "sem", "mean", "prod", "median")
    if agg_function in no_drop_nuisance and not numeric_only:
        # Added numeric_only as part of GH#46560; these do not drop nuisance
        # columns when numeric_only is False
        if using_infer_string:
            msg = f"dtype 'str' does not support operation '{agg_function}'"
            klass = TypeError
        elif agg_function in ("std", "sem"):
            klass = ValueError
            msg = "could not convert string to float: 'one'"
        else:
            klass = TypeError
            msg = re.escape(f"agg function failed [how->{agg_function},dtype->")
        with pytest.raises(klass, match=msg):
            getattr(grouped, agg_function)(numeric_only=numeric_only)
    else:
        result = getattr(grouped, agg_function)(numeric_only=numeric_only)
        if not numeric_only and agg_function == "sum":
            # sum is successful on column B
            columns = ["A", "B", "C", "D"]
        else:
            columns = ["A", "C", "D"]
        expected = getattr(df.loc[:, columns].groupby("A"), agg_function)(
            numeric_only=numeric_only
        )
        tm.assert_frame_equal(result, expected)

