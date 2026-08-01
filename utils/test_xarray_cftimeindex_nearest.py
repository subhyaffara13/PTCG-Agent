
def test_xarray_cftimeindex_nearest():
    # https://github.com/pydata/xarray/issues/3751
    cftime = pytest.importorskip("cftime")
    xarray = pytest.importorskip("xarray")

    times = xarray.date_range("0001", periods=2, use_cftime=True)
    key = cftime.DatetimeGregorian(2000, 1, 1)
    result = times.get_indexer([key], method="nearest")
    expected = 1
    assert result == expected

