
def test_aggregate_categorical_lost_index(func: str):
    # GH: 28641 groupby drops index, when grouping over categorical column with min/max
    ds = Series(["b"], dtype="category").cat.as_ordered()
    df = DataFrame({"A": [1997], "B": ds})
    result = df.groupby("A").agg({"B": func})
    expected = DataFrame({"B": ["b"]}, index=pd.Index([1997], name="A"))

    # ordered categorical dtype should be preserved
    expected["B"] = expected["B"].astype(ds.dtype)

    tm.assert_frame_equal(result, expected)

