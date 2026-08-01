
def test_groupby_non_arithmetic_agg_types(dtype, method, data):
    # GH9311, GH6620
    df = DataFrame(
        [{"a": 1, "b": 1}, {"a": 1, "b": 2}, {"a": 2, "b": 3}, {"a": 2, "b": 4}]
    )

    df["b"] = df.b.astype(dtype)

    if "args" not in data:
        data["args"] = []

    if "out_type" in data:
        out_type = data["out_type"]
    else:
        out_type = dtype

    exp = data["df"]
    df_out = DataFrame(exp)

    df_out["b"] = df_out.b.astype(out_type)
    df_out.set_index("a", inplace=True)

    grpd = df.groupby("a")
    t = getattr(grpd, method)(*data["args"])
    tm.assert_frame_equal(t, df_out)

