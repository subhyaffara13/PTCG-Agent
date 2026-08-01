
def test_groupby_aggregation_empty_group():
    # https://github.com/pandas-dev/pandas/issues/18869
    def func(x):
        if len(x) == 0:
            raise ValueError("length must not be 0")
        return len(x)

    df = DataFrame(
        {"A": pd.Categorical(["a", "a"], categories=["a", "b", "c"]), "B": [1, 1]}
    )
    msg = "length must not be 0"
    with pytest.raises(ValueError, match=msg):
        df.groupby("A", observed=False).agg(func)

