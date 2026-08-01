
def test_seriesbug1():
    assert (1/x).nseries(x, 0, 3) == 1/x
    assert (x + 1/x).nseries(x, 0, 3) == x + 1/x

