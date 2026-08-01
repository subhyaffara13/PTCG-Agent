
def test_maybe_unbox_numpy_scalar_timestamp(unit, using_python_scalars):
    # https://github.com/pandas-dev/pandas/pull/63016
    value = np.datetime64(1, unit)
    expected = Timestamp(1, unit=unit) if using_python_scalars else value
    result = maybe_unbox_numpy_scalar(value)
    assert result == expected
    assert type(result) == type(expected)

