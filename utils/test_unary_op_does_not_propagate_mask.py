
def test_unary_op_does_not_propagate_mask(data, op):
    # https://github.com/pandas-dev/pandas/issues/39943
    data, _ = data
    ser = pd.Series(data)

    if op == "__invert__" and data.dtype.kind == "f":
        # we follow numpy in raising
        msg = "ufunc 'invert' not supported for the input types"
        with pytest.raises(TypeError, match=msg):
            getattr(ser, op)()
        with pytest.raises(TypeError, match=msg):
            getattr(data, op)()
        with pytest.raises(TypeError, match=msg):
            # Check that this is still the numpy behavior
            getattr(data._data, op)()

        return

    result = getattr(ser, op)()
    expected = result.copy(deep=True)
    ser[0] = None
    tm.assert_series_equal(result, expected)

