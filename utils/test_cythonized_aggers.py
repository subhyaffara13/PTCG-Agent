
def test_cythonized_aggers(op_name):
    data = {
        "A": [0, 0, 0, 0, 1, 1, 1, 1, 1, 1.0, np.nan, np.nan],
        "B": ["A", "B"] * 6,
        "C": np.random.default_rng(2).standard_normal(12),
    }
    df = DataFrame(data)
    df.loc[2:10:2, "C"] = np.nan

    op = lambda x: getattr(x, op_name)()

    # single column
    grouped = df.drop(["B"], axis=1).groupby("A")
    exp = {cat: op(group["C"]) for cat, group in grouped}
    exp = DataFrame({"C": exp})
    exp.index.name = "A"
    result = op(grouped)
    tm.assert_frame_equal(result, exp)

    # multiple columns
    grouped = df.groupby(["A", "B"])
    expd = {}
    for (cat1, cat2), group in grouped:
        expd.setdefault(cat1, {})[cat2] = op(group["C"])
    exp = DataFrame(expd).T.stack()
    exp.index.names = ["A", "B"]
    exp.name = "C"

    result = op(grouped)["C"]
    if op_name in ["sum", "prod"]:
        tm.assert_series_equal(result, exp)

