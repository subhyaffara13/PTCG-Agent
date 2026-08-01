
def test_unique_label_indices():
    a = np.random.default_rng(2).integers(1, 1 << 10, 1 << 15).astype(np.intp)

    left = ht.unique_label_indices(a)
    right = np.unique(a, return_index=True)[1]

    tm.assert_numpy_array_equal(left, right, check_dtype=False)

    a[np.random.default_rng(2).choice(len(a), 10)] = -1
    left = ht.unique_label_indices(a)
    right = np.unique(a, return_index=True)[1][1:]
    tm.assert_numpy_array_equal(left, right, check_dtype=False)

