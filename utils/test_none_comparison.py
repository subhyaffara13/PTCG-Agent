
def test_none_comparison(request, series_with_simple_index):
    series = series_with_simple_index

    if len(series) < 1:
        request.applymarker(
            pytest.mark.xfail(reason="Test doesn't make sense on empty data")
        )

    # bug brought up by #1079
    # changed from TypeError in 0.17.0
    series.iloc[0] = np.nan

    # noinspection PyComparisonWithNone
    result = series == None  # noqa: E711
    assert not result.iat[0]
    assert not result.iat[1]

    # noinspection PyComparisonWithNone
    result = series != None  # noqa: E711
    assert result.iat[0]
    assert result.iat[1]

    result = None == series  # noqa: E711
    assert not result.iat[0]
    assert not result.iat[1]

    result = None != series  # noqa: E711
    assert result.iat[0]
    assert result.iat[1]

    if lib.is_np_dtype(series.dtype, "M") or isinstance(series.dtype, DatetimeTZDtype):
        # Following DatetimeIndex (and Timestamp) convention,
        # inequality comparisons with Series[datetime64] raise
        msg = "Invalid comparison"
        with pytest.raises(TypeError, match=msg):
            None > series
        with pytest.raises(TypeError, match=msg):
            series > None
    else:
        result = None > series
        assert not result.iat[0]
        assert not result.iat[1]

        result = series < None
        assert not result.iat[0]
        assert not result.iat[1]

