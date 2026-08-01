
def test_hash_array_mixed(dtype):
    result1 = hash_array(np.array(["3", "4", "All"]))
    result2 = hash_array(np.array([3, 4, "All"], dtype=dtype))

    tm.assert_numpy_array_equal(result1, result2)

