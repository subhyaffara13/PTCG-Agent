
def test_groupby_multiple_columns(df, op):
    data = df
    grouped = data.groupby(["A", "B"])

    result1 = op(grouped)

    keys = []
    values = []
    for n1, gp1 in data.groupby("A"):
        for n2, gp2 in gp1.groupby("B"):
            keys.append((n1, n2))
            values.append(op(gp2.loc[:, ["C", "D"]]))

    mi = MultiIndex.from_tuples(keys, names=["A", "B"])
    expected = pd.concat(values, axis=1).T
    expected.index = mi

    # a little bit crude
    for col in ["C", "D"]:
        result_col = op(grouped[col])
        pivoted = result1[col]
        exp = expected[col]
        tm.assert_series_equal(result_col, exp)
        tm.assert_series_equal(pivoted, exp)

    # test single series works the same
    result = data["C"].groupby([data["A"], data["B"]]).mean()
    expected = data.groupby(["A", "B"]).mean()["C"]

    tm.assert_series_equal(result, expected)

