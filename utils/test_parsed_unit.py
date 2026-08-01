
def test_parsed_unit():
    td = Timedelta("1 Day")
    assert td.unit == "us"

    td = Timedelta("1 Day 2 hours 3 minutes 4 ns")
    assert td.unit == "ns"

    td = Timedelta("1 Day 2:03:04.012345")
    assert td.unit == "us"

    td = Timedelta("1 Day 2:03:04.012345000")
    assert td.unit == "ns"

    # 7 digits after the decimal
    td = Timedelta("1 Day 2:03:04.0123450")
    assert td.unit == "ns"

