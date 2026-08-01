
def test_comparison_for_subclasses(rvalues, op):
    # GH#63205 Ensure subclasses of ndarray are correctly handled in comparison_op
    # Define a custom ndarray subclass
    class TestArray(np.ndarray):
        def __new__(cls, input_array):
            return np.asarray(input_array).view(cls)

        def __array_finalize__(self, obj) -> None:
            self._is_test_array = True

    def expected_with_na_handling(lvalues, rvalues, op):
        # Similar to comparison_op, handle zerodim arrays with na value separately
        if (rvalues.ndim == 0) and isna(rvalues.item()):
            # numpy does not like comparisons vs None
            if op is operator.ne:
                return np.ones(lvalues.shape, dtype=bool)
            else:
                return np.zeros(lvalues.shape, dtype=bool)
        return op(lvalues, rvalues)

    # Define test data
    lvalues = [1, 2, 3]

    # Test with both ndarray and TestArray
    result = comparison_op(np.array(lvalues), np.array(rvalues), op)
    expected = expected_with_na_handling(np.array(lvalues), np.array(rvalues), op)
    tm.assert_numpy_array_equal(result, expected)

    result = comparison_op(TestArray(lvalues), TestArray(rvalues), op)
    expected = expected_with_na_handling(TestArray(lvalues), TestArray(rvalues), op)
    tm.assert_numpy_array_equal(result, expected)

