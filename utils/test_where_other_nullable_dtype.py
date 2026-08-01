
def test_where_other_nullable_dtype():
    # GH#49052 DataFrame.where should return nullable dtype when
    # other is a Series with nullable dtype, matching Series.where behavior
    df = DataFrame([1, 2, 3], dtype="int64")
    other = Series([pd.NA, pd.NA, pd.NA], dtype="Int64")
    result = df.where(df > 1, other, axis=0)
    expected = DataFrame({0: Series([pd.NA, 2, 3], dtype="Int64")})
    tm.assert_frame_equal(result, expected)

