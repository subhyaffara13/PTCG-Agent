
def test_sinsinbug():
    assert sin(sin(x)).nseries(x, 0, 8) == x - x**3/3 + x**5/10 - 8*x**7/315 + O(x**8)

