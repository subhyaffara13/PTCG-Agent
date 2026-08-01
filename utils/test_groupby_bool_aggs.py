
def test_groupby_bool_aggs(skipna, all_boolean_reductions, vals):
    df = DataFrame({"key": ["a"] * 3 + ["b"] * 3, "val": vals * 2})

    # Figure out expectation using Python builtin
    exp = getattr(builtins, all_boolean_reductions)(vals)

    # edge case for missing data with skipna and 'any'
    if skipna and all(isna(vals)) and all_boolean_reductions == "any":
        exp = False

    expected = DataFrame(
        [exp] * 2, columns=["val"], index=pd.Index(["a", "b"], name="key")
    )
    result = getattr(df.groupby("key"), all_boolean_reductions)(skipna=skipna)
    tm.assert_frame_equal(result, expected)

