
def test_hash_object_none_key():
    # https://github.com/pandas-dev/pandas/issues/30887
    result = pd.util.hash_pandas_object(Series(["a", "b"]), hash_key=None)
    expected = Series([4578374827886788867, 17338122309987883691], dtype="uint64")
    tm.assert_series_equal(result, expected)

