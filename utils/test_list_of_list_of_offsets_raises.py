
def test_list_of_list_of_offsets_raises():
    # see gh-29049
    # Test that the offsets of offsets are forbidden
    holiday1 = Holiday(
        "Holiday1",
        month=USThanksgivingDay.month,
        day=USThanksgivingDay.day,
        offset=[USThanksgivingDay.offset, DateOffset(1)],
    )
    msg = "Only BaseOffsets and flat lists of them are supported for offset."
    with pytest.raises(ValueError, match=msg):
        Holiday(
            "Holiday2",
            month=holiday1.month,
            day=holiday1.day,
            offset=[holiday1.offset, DateOffset(3)],
        )

