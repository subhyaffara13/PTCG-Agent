
def test_stack_unstack_empty_frame(dropna, fill_value, future_stack):
    # GH 36113
    if future_stack and dropna is not lib.no_default:
        with pytest.raises(ValueError, match="dropna must be unspecified"):
            DataFrame(dtype=np.int64).stack(
                dropna=dropna, future_stack=future_stack
            ).unstack(fill_value=fill_value)
    else:
        result = (
            DataFrame(dtype=np.int64)
            .stack(dropna=dropna, future_stack=future_stack)
            .unstack(fill_value=fill_value)
        )
        expected = DataFrame(dtype=np.int64)
        tm.assert_frame_equal(result, expected)

