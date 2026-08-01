
def test_ensure_string_array_copy():
    # ensure the original array is not modified in case of copy=False with
    # pickle-roundtripped object dtype array
    # https://github.com/pandas-dev/pandas/issues/54654
    arr = np.array(["a", None], dtype=object)
    arr = pickle.loads(pickle.dumps(arr))
    result = lib.ensure_string_array(arr, copy=False)
    assert not np.shares_memory(arr, result)
    assert arr[1] is None
    assert result[1] is np.nan

