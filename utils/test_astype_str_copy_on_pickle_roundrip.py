
def test_astype_str_copy_on_pickle_roundrip():
    # TODO(infer_string) this test can be removed after 3.0 (once str is the default)
    # https://github.com/pandas-dev/pandas/issues/54654
    # ensure_string_array may alter array inplace
    base = Series(np.array([(1, 2), None, 1], dtype="object"))
    base_copy = pickle.loads(pickle.dumps(base))
    base_copy.astype(str)
    tm.assert_series_equal(base, base_copy)

