
def test_N17():
    # currently only univariate inequalities are supported
    assert solveset((x + y > 0, x - y < 0), (x, y)) == (abs(x) < y)

