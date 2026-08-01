
def test_dti_resolution(request, tz_naive_fixture, freq, expected):
    tz = tz_naive_fixture
    if freq == "YE" and ((not IS64) or WASM) and isinstance(tz, tzlocal):
        request.applymarker(
            pytest.mark.xfail(reason="OverflowError inside tzlocal past 2038")
        )

    idx = date_range(start="2013-04-01", periods=30, freq=freq, tz=tz)
    assert idx.resolution == expected

