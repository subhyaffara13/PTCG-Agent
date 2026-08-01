
def test_combine_first_timestamp_bug_NaT():
    # GH28481
    frame = DataFrame([[pd.NaT, pd.NaT]], columns=["a", "b"])
    other = DataFrame(
        [[datetime(2020, 1, 1), datetime(2020, 1, 2)]], columns=["b", "c"]
    )

    result = frame.combine_first(other)
    expected = DataFrame(
        [[pd.NaT, datetime(2020, 1, 1), datetime(2020, 1, 2)]], columns=["a", "b", "c"]
    )

    tm.assert_frame_equal(result, expected)

