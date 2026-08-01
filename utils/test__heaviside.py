
def test_Heaviside():
    sT(Heaviside(x), "Heaviside(Symbol('x'))")
    sT(Heaviside(x, 1), "Heaviside(Symbol('x'), Integer(1))")


def test_Heaviside():
    assert str(Heaviside(x)) == str(Heaviside(x, S.Half)) == "Heaviside(x)"
    assert str(Heaviside(x, 1)) == "Heaviside(x, 1)"

