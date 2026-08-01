
def test_get_state():
    x, y = symbols('x y')
    d = Density([Ket(0), x], [Ket(1), y])
    states = (d.get_state(0), d.get_state(1))
    assert states[0] == Ket(0) and states[1] == Ket(1)

