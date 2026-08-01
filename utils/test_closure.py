
def test_closure():
    assert Interval(0, 1, False, True).closure == Interval(0, 1, False, False)

