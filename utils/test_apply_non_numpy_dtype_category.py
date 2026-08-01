
def test_apply_non_numpy_dtype_category():
    df = DataFrame({"dt": ["a", "b", "c", "a"]}, dtype="category")
    result = df.apply(lambda x: x)
    tm.assert_frame_equal(result, df)

