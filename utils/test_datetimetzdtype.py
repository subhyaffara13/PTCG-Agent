
def test_datetimetzdtype(tz, unit):
    # GH 54239
    tz_data = (
        pd.date_range("2018-01-01", periods=5, freq="D").tz_localize(tz).as_unit(unit)
    )
    df = pd.DataFrame({"ts_tz": tz_data})
    with tm.assert_produces_warning(match="Interchange"):
        tm.assert_frame_equal(df, from_dataframe(df.__dataframe__()))

