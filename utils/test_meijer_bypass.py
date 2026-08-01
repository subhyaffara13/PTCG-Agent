
def test_meijer_bypass():
    # totally bypass meijerg machinery when dealing
    # with Piecewise in integrate
    assert Piecewise((1, x < 4), (0, True)).integrate((x, oo, 1)) == -3

