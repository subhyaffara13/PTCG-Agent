
def test_resample_interpolate_inplace_deprecated():
    # GH#58690
    dti = date_range(datetime(2005, 1, 1), datetime(2005, 1, 10), freq="D")

    df = DataFrame(range(len(dti)), index=dti)
    rs = df.resample("1min")
    msg = "The 'inplace' keyword in DatetimeIndexResampler.interpolate"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        rs.interpolate(inplace=False)

    msg2 = "Cannot interpolate inplace on a resampled object"
    with pytest.raises(ValueError, match=msg2):
        with tm.assert_produces_warning(Pandas4Warning, match=msg):
            rs.interpolate(inplace=True)

