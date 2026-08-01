
def test_item_from_zerodim_for_subclasses():
    # GH#62981 Ensure item_from_zerodim preserves subclasses of ndarray
    # Define a custom ndarray subclass
    class TestArray(np.ndarray):
        def __new__(cls, input_array):
            return np.asarray(input_array).view(cls)

        def __array_finalize__(self, obj) -> None:
            self._is_test_array = True

    # Define test data
    val_0_dim = 1
    val_1_dim = [1, 2, 3]

    # 0-dim and 1-dim numpy arrays
    arr_0_dim = np.array(val_0_dim)
    arr_1_dim = np.array(val_1_dim)

    # 0-dim and 1-dim TestArray arrays
    test_arr_0_dim = TestArray(val_0_dim)
    test_arr_1_dim = TestArray(val_1_dim)

    # Check that behavior did not change for regular numpy arrays
    # Test with regular numpy 0-dim array
    result = lib.item_from_zerodim(arr_0_dim)
    expected = val_0_dim
    assert result == expected
    assert np.isscalar(result)

    # Test with regular numpy 1-dim array
    result = lib.item_from_zerodim(arr_1_dim)
    expected = arr_1_dim
    tm.assert_numpy_array_equal(result, expected)
    assert isinstance(result, np.ndarray)

    # Check that behaviour for subclasses now is as expected
    # Test with TestArray 0-dim array
    result = lib.item_from_zerodim(test_arr_0_dim)
    expected = test_arr_0_dim
    assert result == expected
    assert isinstance(result, TestArray)

    # Test with TestArray 1-dim array
    result = lib.item_from_zerodim(test_arr_1_dim)
    expected = test_arr_1_dim
    assert np.all(result == expected)
    assert isinstance(result, TestArray)

