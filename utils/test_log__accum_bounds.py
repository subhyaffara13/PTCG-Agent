
def test_log_AccumBounds():
    assert log(AccumBounds(1, E)) == AccumBounds(0, 1)
    assert log(AccumBounds(0, E)) == AccumBounds(-oo, 1)
    assert log(AccumBounds(-1, E)) == S.NaN
    assert log(AccumBounds(0, oo)) == AccumBounds(-oo, oo)
    assert log(AccumBounds(-oo, 0)) == S.NaN
    assert log(AccumBounds(-oo, oo)) == S.NaN

