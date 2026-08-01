
def test_cython_transform_frame(request, op, args, targop, df_fix, gb_target):
    df = request.getfixturevalue(df_fix)
    gb = df.groupby(group_keys=False, **gb_target)

    if op != "shift" and "int" not in gb_target:
        # numeric apply fastpath promotes dtype so have
        # to apply separately and concat
        i = gb[["int"]].apply(targop)
        f = gb[["float", "float_missing"]].apply(targop)
        expected = concat([f, i], axis=1)
    else:
        expected = gb.apply(targop)

    expected = expected.sort_index(axis=1)
    if op == "shift":
        expected["string_missing"] = expected["string_missing"].fillna(np.nan)
        by = gb_target.get("by")
        if not isinstance(by, (str, list)) or (by != "string" and "string" not in by):
            expected["string"] = expected["string"].fillna(np.nan)

    result = gb[expected.columns].transform(op, *args).sort_index(axis=1)
    tm.assert_frame_equal(result, expected)
    result = getattr(gb[expected.columns], op)(*args).sort_index(axis=1)
    tm.assert_frame_equal(result, expected)

