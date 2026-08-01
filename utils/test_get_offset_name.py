
def test_get_offset_name():
    assert (
        makeFY5253LastOfMonthQuarter(
            weekday=1, startingMonth=3, qtr_with_extra_week=4
        ).freqstr
        == "REQ-L-MAR-TUE-4"
    )
    assert (
        makeFY5253NearestEndMonthQuarter(
            weekday=1, startingMonth=3, qtr_with_extra_week=3
        ).freqstr
        == "REQ-N-MAR-TUE-3"
    )

