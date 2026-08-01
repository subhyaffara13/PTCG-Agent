
def test_num2timedelta(x, tdelta):
    dt = mdates.num2timedelta(x)
    assert dt == tdelta

