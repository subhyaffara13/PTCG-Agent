
def test_cython_transform_frame_column(
    request, op, args, targop, df_fix, gb_target, column
):
    df = request.getfixturevalue(df_fix)
    gb = df.groupby(group_keys=False, **gb_target)
    c = column
    if (
        c not in ["float", "int", "float_missing"]
        and op != "shift"
        and not (c == "timedelta" and op == "cumsum")
    ):
        msg = "|".join(
            [
                "does not support .* operations",
                "does not support operation",
                ".* is not supported for object dtype",
                "is not implemented for this dtype",
                ".* is not supported for str dtype",
            ]
        )
        with pytest.raises(TypeError, match=msg):
            gb[c].transform(op)
        with pytest.raises(TypeError, match=msg):
            getattr(gb[c], op)()
    else:
        expected = gb[c].apply(targop)
        expected.name = c
        if c in ["string_missing", "string"]:
            expected = expected.fillna(np.nan)

        res = gb[c].transform(op, *args)
        tm.assert_series_equal(expected, res)
        res2 = getattr(gb[c], op)(*args)
        tm.assert_series_equal(expected, res2)

