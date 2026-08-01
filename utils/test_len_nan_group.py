
def test_len_nan_group():
    # issue 11016
    df = DataFrame({"a": [np.nan] * 3, "b": [1, 2, 3]})
    assert len(df.groupby("a")) == 0
    assert len(df.groupby("b")) == 3
    assert len(df.groupby(["a", "b"])) == 0

