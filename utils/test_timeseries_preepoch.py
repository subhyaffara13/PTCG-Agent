
def test_timeseries_preepoch(temp_h5_path, request):
    dr = bdate_range("1/1/1940", "1/1/1960")
    ts = Series(np.random.default_rng(2).standard_normal(len(dr)), index=dr)
    try:
        _check_roundtrip(ts, tm.assert_series_equal, path=temp_h5_path)
    except OverflowError:
        if is_platform_windows():
            request.applymarker(
                pytest.mark.xfail("known failure on some windows platforms")
            )
        raise

