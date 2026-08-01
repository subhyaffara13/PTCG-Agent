
def test_delta_to_tick():
    delta = timedelta(3)

    tick = delta_to_tick(delta)
    assert tick == offsets.Hour(72)

    td = Timedelta(nanoseconds=5)
    tick = delta_to_tick(td)
    assert tick == Nano(5)

