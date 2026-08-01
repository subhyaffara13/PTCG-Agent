
def test_interior():
    assert Interval(0, 1, False, True).interior == Interval(0, 1, True, True)

