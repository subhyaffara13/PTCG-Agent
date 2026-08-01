
def test_unique_arena_strings():
    # _unique_hash has a dedicated StringDType loop
    vals = [f"{'u' * 16}{i % 7:04d}" for i in range(50)] + ["ab", "ab", ""]
    arr = np.array(vals, dtype="T")
    arr_u = arr.astype("U20")
    assert_array_equal(np.unique(arr), np.unique(arr_u))
    assert_array_equal(np.sort(np.unique_values(arr)), np.unique(arr_u))

    # index/inverse/counts go through the sort-based path
    res = np.unique(
        arr, return_index=True, return_inverse=True, return_counts=True
    )
    expected = np.unique(
        arr_u, return_index=True, return_inverse=True, return_counts=True
    )
    for r, e in zip(res, expected):
        assert_array_equal(r, e)

