
def test_map_box():
    # ufunc will not be boxed. Same test cases as the test_map_box
    df = DataFrame(
        {
            "a": [Timestamp("2011-01-01"), Timestamp("2011-01-02")],
            "b": [
                Timestamp("2011-01-01", tz="US/Eastern"),
                Timestamp("2011-01-02", tz="US/Eastern"),
            ],
            "c": [pd.Timedelta("1 days"), pd.Timedelta("2 days")],
            "d": [
                pd.Period("2011-01-01", freq="M"),
                pd.Period("2011-01-02", freq="M"),
            ],
        }
    )

    result = df.map(lambda x: type(x).__name__)
    expected = DataFrame(
        {
            "a": ["Timestamp", "Timestamp"],
            "b": ["Timestamp", "Timestamp"],
            "c": ["Timedelta", "Timedelta"],
            "d": ["Period", "Period"],
        }
    )
    tm.assert_frame_equal(result, expected)

