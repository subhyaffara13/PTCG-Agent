
def test_custom_businesshour_weekmask_and_holidays(weekmask, expected_time, mult):
    # GH 23542
    holidays = ["2018-11-09"]
    bh = CustomBusinessHour(
        start="08:00", end="17:00", weekmask=weekmask, holidays=holidays
    )
    result = Timestamp("2018-11-08 08:00") + mult * bh
    expected = Timestamp(expected_time)
    assert result == expected

