
def test_maybe_unbox_numpy_scalar_datetime(unit, using_python_scalars):
    # https://github.com/pandas-dev/pandas/pull/63016
    value = np.timedelta64(1, unit)
    expected = Timedelta(1, unit=unit) if using_python_scalars else value
    result = maybe_unbox_numpy_scalar(value)
    assert result == expected
    assert type(result) == type(expected)

