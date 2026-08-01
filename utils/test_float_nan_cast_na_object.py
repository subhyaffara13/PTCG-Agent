
def test_float_nan_cast_na_object():
    # gh-28157
    dt = np.dtypes.StringDType(na_object=np.nan)
    arr1 = np.full((1,), fill_value=np.nan, dtype=dt)
    arr2 = np.full_like(arr1, fill_value=np.nan)

    assert arr1.item() is np.nan
    assert arr2.item() is np.nan

    inp = [1.2, 2.3, np.nan]
    arr = np.array(inp).astype(dt)
    assert arr[2] is np.nan
    assert arr[0] == '1.2'

