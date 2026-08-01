
def test_stack_empty_level(dropna, future_stack, int_frame):
    # GH 60740
    if future_stack and dropna is not lib.no_default:
        with pytest.raises(ValueError, match="dropna must be unspecified"):
            DataFrame(dtype=np.int64).stack(dropna=dropna, future_stack=future_stack)
    else:
        expected = int_frame
        result = int_frame.copy().stack(
            level=[], dropna=dropna, future_stack=future_stack
        )
        tm.assert_frame_equal(result, expected)

        expected = DataFrame()
        result = DataFrame().stack(level=[], dropna=dropna, future_stack=future_stack)
        tm.assert_frame_equal(result, expected)

