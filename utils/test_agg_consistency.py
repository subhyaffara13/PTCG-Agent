
def test_agg_consistency():
    # make sure that we are consistent across
    # similar aggregations with and w/o selection list
    df = DataFrame(
        np.random.default_rng(2).standard_normal((1000, 3)),
        index=date_range("1/1/2012", freq="s", periods=1000),
        columns=["A", "B", "C"],
    )

    r = df.resample("3min")

    msg = r"Label\(s\) \['r1', 'r2'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        r.agg({"r1": "mean", "r2": "sum"})


def test_agg_consistency(step):
    df = DataFrame({"A": range(5), "B": range(0, 10, 2)})
    r = df.rolling(window=3, step=step)

    result = r.agg([np.sum, np.mean]).columns
    expected = MultiIndex.from_product([list("AB"), ["sum", "mean"]])
    tm.assert_index_equal(result, expected)

    result = r["A"].agg([np.sum, np.mean]).columns
    expected = Index(["sum", "mean"])
    tm.assert_index_equal(result, expected)

    result = r.agg({"A": [np.sum, np.mean]}).columns
    expected = MultiIndex.from_tuples([("A", "sum"), ("A", "mean")])
    tm.assert_index_equal(result, expected)


def test_agg_consistency():
    # agg with ([]) and () not consistent
    # GH 6715
    def P1(a):
        return np.percentile(a.dropna(), q=1)

    df = DataFrame(
        {
            "col1": [1, 2, 3, 4],
            "col2": [10, 25, 26, 31],
            "date": [
                dt.date(2013, 2, 10),
                dt.date(2013, 2, 10),
                dt.date(2013, 2, 11),
                dt.date(2013, 2, 11),
            ],
        }
    )

    g = df.groupby("date")

    expected = g.agg([P1])
    expected.columns = expected.columns.levels[0]

    result = g.agg(P1)
    tm.assert_frame_equal(result, expected)

