
def test_stack_empty_frame(dropna, future_stack):
    # GH 36113
    levels = [pd.RangeIndex(0), pd.RangeIndex(0)]
    expected = Series(dtype=np.float64, index=MultiIndex(levels=levels, codes=[[], []]))
    if future_stack and dropna is not lib.no_default:
        with pytest.raises(ValueError, match="dropna must be unspecified"):
            DataFrame(dtype=np.float64).stack(dropna=dropna, future_stack=future_stack)
    else:
        result = DataFrame(dtype=np.float64).stack(
            dropna=dropna, future_stack=future_stack
        )
        tm.assert_series_equal(result, expected)

