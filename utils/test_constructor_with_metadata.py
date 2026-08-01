
def test_constructor_with_metadata():
    # https://github.com/pandas-dev/pandas/pull/54922
    # https://github.com/pandas-dev/pandas/issues/55120
    df = MySubclassWithMetadata(
        np.random.default_rng(2).random((5, 3)), columns=["A", "B", "C"]
    )
    subset = df[["A", "B"]]
    assert isinstance(subset, MySubclassWithMetadata)

