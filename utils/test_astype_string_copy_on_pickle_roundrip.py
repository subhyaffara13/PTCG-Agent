
def test_astype_string_copy_on_pickle_roundrip(any_string_dtype):
    # https://github.com/pandas-dev/pandas/issues/54654
    # ensure_string_array may alter array inplace
    base = Series(np.array([(1, 2), None, 1], dtype="object"))
    base_copy = pickle.loads(pickle.dumps(base))
    base_copy.astype(any_string_dtype)
    tm.assert_series_equal(base, base_copy)

