
def test_exclude_date_value_error():
    msg = "exclude_dates must be None or of type DatetimeIndex."

    with pytest.raises(ValueError, match=msg):
        exclude = [
            Timestamp("2025-06-10"),
            Timestamp("2026-06-10"),
        ]
        Holiday("National Ice Tea Day", month=6, day=10, exclude_dates=exclude)

