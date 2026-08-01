
def test_both_offset_observance_raises():
    # see gh-10217
    msg = "Cannot use both offset and observance"
    with pytest.raises(NotImplementedError, match=msg):
        Holiday(
            "Cyber Monday",
            month=11,
            day=1,
            offset=[DateOffset(weekday=SA(4))],
            observance=next_monday,
        )

