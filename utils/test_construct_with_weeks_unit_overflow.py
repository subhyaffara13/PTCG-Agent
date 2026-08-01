
def test_construct_with_weeks_unit_overflow():
    # GH#47268 don't silently wrap around
    msg = "1000000000000000000 weeks"
    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        Timedelta(1000000000000000000, unit="W")

    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        Timedelta(1000000000000000000.0, unit="W")

