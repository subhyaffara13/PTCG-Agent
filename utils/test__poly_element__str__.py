
def test_PolyElement__str__():
    x, y = symbols('x, y')

    for dom in [ZZ, QQ, ZZ[x], ZZ[x,y], ZZ[x][y]]:
        R, t = ring('t', dom)
        assert str(2*t**2 + 1) == '2*t**2 + 1'

    for dom in [EX, EX[x]]:
        R, t = ring('t', dom)
        assert str(2*t**2 + 1) == 'EX(2)*t**2 + EX(1)'

