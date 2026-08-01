
def test_shift_bfill_ffill_tz(tz_naive_fixture, op, expected):
    # GH19995, GH27992: Check that timezone does not drop in shift, bfill, and ffill
    tz = tz_naive_fixture
    data = {
        "id": ["A", "B", "A", "B", "A", "B"],
        "time": [
            Timestamp("2019-01-01 12:00:00"),
            Timestamp("2019-01-01 12:30:00"),
            None,
            None,
            Timestamp("2019-01-01 14:00:00"),
            Timestamp("2019-01-01 14:30:00"),
        ],
    }
    df = DataFrame(data).assign(time=lambda x: x.time.dt.tz_localize(tz))

    grouped = df.groupby("id")
    result = getattr(grouped, op)()
    expected = DataFrame(expected).assign(time=lambda x: x.time.dt.tz_localize(tz))
    tm.assert_frame_equal(result, expected)

