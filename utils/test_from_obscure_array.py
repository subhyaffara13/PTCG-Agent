
def test_from_obscure_array(dtype, box):
    # GH#24539 recognize e.g xarray, dask, ...
    # Note: we dont do this for PeriodArray bc _from_sequence won't accept
    #  an array of integers
    # TODO: could check with arraylike of Period objects
    # GH#24539 recognize e.g xarray, dask, ...
    arr = np.array([1, 2, 3], dtype=np.int64)
    if box == "dask":
        da = pytest.importorskip("dask.array")
        data = da.array(arr)
    elif box == "xarray":
        xr = pytest.importorskip("xarray")
        data = xr.DataArray(arr)
    else:
        data = box(arr)

    func = {"M8[ns]": pd.to_datetime, "m8[ns]": pd.to_timedelta}[dtype]
    result = func(arr).array
    expected = func(data).array
    tm.assert_equal(result, expected)

    # Let's check the Indexes while we're here
    idx_cls = {"M8[ns]": DatetimeIndex, "m8[ns]": TimedeltaIndex}[dtype]
    result = idx_cls(arr)
    expected = idx_cls(data)
    tm.assert_index_equal(result, expected)

