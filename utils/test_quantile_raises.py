
def test_quantile_raises():
    df = DataFrame([["foo", "a"], ["foo", "b"], ["foo", "c"]], columns=["key", "val"])

    msg = "dtype '(object|str)' does not support operation 'quantile'"
    with pytest.raises(TypeError, match=msg):
        df.groupby("key").quantile()

