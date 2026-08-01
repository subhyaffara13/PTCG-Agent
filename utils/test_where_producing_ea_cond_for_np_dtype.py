
def test_where_producing_ea_cond_for_np_dtype():
    # GH#44014
    df = DataFrame({"a": Series([1, pd.NA, 2], dtype="Int64"), "b": [1, 2, 3]})
    result = df.where(lambda x: x.apply(lambda y: y > 1, axis=1))
    expected = DataFrame(
        {"a": Series([pd.NA, pd.NA, 2], dtype="Int64"), "b": [np.nan, 2, 3]}
    )
    tm.assert_frame_equal(result, expected)

