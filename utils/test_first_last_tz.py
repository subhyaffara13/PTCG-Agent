
def test_first_last_tz(data, expected_first, expected_last):
    # GH15884
    # Test that the timezone is retained when calling first
    # or last on groupby with as_index=False

    df = DataFrame(data)

    result = df.groupby("id", as_index=False).first()
    expected = DataFrame(expected_first)
    cols = ["id", "time", "foo"]
    tm.assert_frame_equal(result[cols], expected[cols])

    result = df.groupby("id", as_index=False)["time"].first()
    tm.assert_frame_equal(result, expected[["id", "time"]])

    result = df.groupby("id", as_index=False).last()
    expected = DataFrame(expected_last)
    cols = ["id", "time", "foo"]
    tm.assert_frame_equal(result[cols], expected[cols])

    result = df.groupby("id", as_index=False)["time"].last()
    tm.assert_frame_equal(result, expected[["id", "time"]])

