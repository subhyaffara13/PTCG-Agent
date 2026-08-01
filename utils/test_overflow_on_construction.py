
def test_overflow_on_construction():
    # GH#3374
    value = Timedelta("1day").as_unit("ns")._value * 20169940
    msg = "Cannot cast 1742682816000000000000 from ns to 'ns' without overflow"
    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        Timedelta(value)

    # xref GH#17637
    # used to overflows before we changed output unit to "s"
    td = Timedelta(7 * 19999, unit="D")
    assert td.unit == "s"

    # used to overflow before non-ns support
    td = Timedelta(timedelta(days=13 * 19999))
    assert td._creso == NpyDatetimeUnit.NPY_FR_us.value
    assert td.days == 13 * 19999

