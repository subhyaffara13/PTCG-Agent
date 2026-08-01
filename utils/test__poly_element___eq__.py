
def test_PolyElement___eq__():
    R, x, y = ring("x,y", ZZ, lex)

    assert ((x*y + 5*x*y) == 6) == False
    assert ((x*y + 5*x*y) == 6*x*y) == True
    assert (6 == (x*y + 5*x*y)) == False
    assert (6*x*y == (x*y + 5*x*y)) == True

    assert ((x*y - x*y) == 0) == True
    assert (0 == (x*y - x*y)) == True

    assert ((x*y - x*y) == 1) == False
    assert (1 == (x*y - x*y)) == False

    assert ((x*y - x*y) == 1) == False
    assert (1 == (x*y - x*y)) == False

    assert ((x*y + 5*x*y) != 6) == True
    assert ((x*y + 5*x*y) != 6*x*y) == False
    assert (6 != (x*y + 5*x*y)) == True
    assert (6*x*y != (x*y + 5*x*y)) == False

    assert ((x*y - x*y) != 0) == False
    assert (0 != (x*y - x*y)) == False

    assert ((x*y - x*y) != 1) == True
    assert (1 != (x*y - x*y)) == True

    assert R.one == QQ(1, 1) == R.one
    assert R.one == 1 == R.one

    Rt, t = ring("t", ZZ)
    R, x, y = ring("x,y", Rt)

    assert (t**3*x/x == t**3) == True
    assert (t**3*x/x == t**4) == False

