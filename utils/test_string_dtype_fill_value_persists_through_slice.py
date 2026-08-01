
def test_string_dtype_fill_value_persists_through_slice():
    # Regression test for gh-29421: .fill_value survives slicing/viewing
    dt = np.dtypes.StringDType()
    arr = np.ma.MaskedArray(
        ['a', 'b', 'c'],
        mask=[True, False, True],
        dtype=dt
    )
    arr.fill_value = 'Z'
    # slice triggers __array_finalize__
    sub = arr[1:]
    # the slice should carry the same fill_value and behavior
    assert isinstance(sub.fill_value, str)
    assert sub.fill_value == 'Z'
    assert sub.filled().tolist() == ['b', 'Z']

