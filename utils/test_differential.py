
def test_differential():
    xdy = R2.x*R2.dy
    dxdy = Differential(xdy)
    assert xdy.rcall(None) == xdy
    assert dxdy(R2.e_x, R2.e_y) == 1
    assert dxdy(R2.e_x, R2.x*R2.e_y) == R2.x
    assert Differential(dxdy) == 0

