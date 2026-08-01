
def test_from_tick_reso():
    tick = offsets.Nano()
    assert Timedelta(tick)._creso == NpyDatetimeUnit.NPY_FR_ns.value

    tick = offsets.Micro()
    assert Timedelta(tick)._creso == NpyDatetimeUnit.NPY_FR_us.value

    tick = offsets.Milli()
    assert Timedelta(tick)._creso == NpyDatetimeUnit.NPY_FR_ms.value

    tick = offsets.Second()
    assert Timedelta(tick)._creso == NpyDatetimeUnit.NPY_FR_s.value

    # everything above Second gets cast to the closest supported reso: second
    tick = offsets.Minute()
    assert Timedelta(tick)._creso == NpyDatetimeUnit.NPY_FR_s.value

    tick = offsets.Hour()
    assert Timedelta(tick)._creso == NpyDatetimeUnit.NPY_FR_s.value

    tick = offsets.Day()
    msg = (
        "Value must be Timedelta, string, integer, float, timedelta "
        "or convertible, not Day"
    )
    with pytest.raises(ValueError, match=msg):
        # GH#41943 Day is no longer a Tick
        Timedelta(tick)

