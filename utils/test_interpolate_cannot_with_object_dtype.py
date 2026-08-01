
def test_interpolate_cannot_with_object_dtype():
    df = DataFrame({"a": ["a", np.nan, "c"], "b": 1})
    df["a"] = df["a"].astype(object)

    msg = "DataFrame cannot interpolate with object dtype"
    with pytest.raises(TypeError, match=msg):
        df.interpolate()

