
def test_merge_categorical_key_recursion():
    # GH#56376
    lt = CategoricalDtype(categories=np.asarray([1, 2, 3], dtype="int64"))
    rt = CategoricalDtype(categories=np.asarray([1, 2, 3], dtype="float64"))
    left = DataFrame({"key": Series([1, 2], dtype=lt)})
    right = DataFrame({"key": Series([1, 3], dtype=rt)})

    result = left.merge(right, on="key", how="outer")
    expected = left.astype("int64").merge(
        right.astype("float64"), on="key", how="outer"
    )
    tm.assert_frame_equal(result, expected)

