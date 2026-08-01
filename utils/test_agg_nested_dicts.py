
def test_agg_nested_dicts():
    index = date_range(datetime(2005, 1, 1), datetime(2005, 1, 10), freq="D")
    index.name = "date"
    df = DataFrame(
        np.random.default_rng(2).random((10, 2)), columns=list("AB"), index=index
    )
    df_col = df.reset_index()
    df_mult = df_col.copy()
    df_mult.index = pd.MultiIndex.from_arrays(
        [range(10), df.index], names=["index", "date"]
    )
    r = df.resample("2D")
    cases = [
        r,
        df_col.resample("2D", on="date"),
        df_mult.resample("2D", level="date"),
        df.groupby(pd.Grouper(freq="2D")),
    ]

    msg = "nested renamer is not supported"
    for t in cases:
        with pytest.raises(pd.errors.SpecificationError, match=msg):
            t.aggregate({"r1": {"A": ["mean", "sum"]}, "r2": {"B": ["mean", "sum"]}})

    for t in cases:
        with pytest.raises(pd.errors.SpecificationError, match=msg):
            t[["A", "B"]].agg(
                {"A": {"ra": ["mean", "std"]}, "B": {"rb": ["mean", "std"]}}
            )

        with pytest.raises(pd.errors.SpecificationError, match=msg):
            t.agg({"A": {"ra": ["mean", "std"]}, "B": {"rb": ["mean", "std"]}})


def test_agg_nested_dicts():
    # API change for disallowing these types of nested dicts
    df = DataFrame({"A": range(5), "B": range(0, 10, 2)})
    r = df.rolling(window=3)

    msg = "nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        r.aggregate({"r1": {"A": ["mean", "sum"]}, "r2": {"B": ["mean", "sum"]}})

    expected = concat(
        [r["A"].mean(), r["A"].std(), r["B"].mean(), r["B"].std()], axis=1
    )
    expected.columns = MultiIndex.from_tuples(
        [("ra", "mean"), ("ra", "std"), ("rb", "mean"), ("rb", "std")]
    )
    with pytest.raises(SpecificationError, match=msg):
        r[["A", "B"]].agg({"A": {"ra": ["mean", "std"]}, "B": {"rb": ["mean", "std"]}})

    with pytest.raises(SpecificationError, match=msg):
        r.agg({"A": {"ra": ["mean", "std"]}, "B": {"rb": ["mean", "std"]}})


def test_agg_nested_dicts():
    # API change for disallowing these types of nested dicts
    df = DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "two", "two", "two", "one", "two"],
            "C": np.random.default_rng(2).standard_normal(8) + 1.0,
            "D": np.arange(8),
        }
    )

    g = df.groupby(["A", "B"])

    msg = r"nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        g.aggregate({"r1": {"C": ["mean", "sum"]}, "r2": {"D": ["mean", "sum"]}})

    with pytest.raises(SpecificationError, match=msg):
        g.agg({"C": {"ra": ["mean", "std"]}, "D": {"rb": ["mean", "std"]}})

    # same name as the original column
    # GH9052
    with pytest.raises(SpecificationError, match=msg):
        g["D"].agg({"result1": np.sum, "result2": np.mean})

    with pytest.raises(SpecificationError, match=msg):
        g["D"].agg({"D": np.sum, "result2": np.mean})

