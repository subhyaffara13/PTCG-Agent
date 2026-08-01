
def test_ewma_with_times_variable_spacing(tz_aware_fixture, unit, adjust):
    # GH 54328
    tz = tz_aware_fixture
    halflife = "23 days"
    times = (
        DatetimeIndex(["2020-01-01", "2020-01-10T00:04:05", "2020-02-23T05:00:23"])
        .tz_localize(tz)
        .as_unit(unit)
    )
    data = np.arange(3)
    df = DataFrame(data)
    result = df.ewm(halflife=halflife, times=times, adjust=adjust).mean()
    if adjust:
        expected = DataFrame([0.0, 0.5674161888241773, 1.545239952073459])
    else:
        expected = DataFrame([0.0, 0.23762518642226227, 1.534926369128742])
    tm.assert_frame_equal(result, expected)

