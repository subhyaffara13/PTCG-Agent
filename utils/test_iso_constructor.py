
def test_iso_constructor(fmt, exp):
    assert Timedelta(fmt) == exp

