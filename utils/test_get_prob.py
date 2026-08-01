
def test_get_prob():
    x, y = symbols('x y')
    d = Density([Ket(0), x], [Ket(1), y])
    probs = (d.get_prob(0), d.get_prob(1))
    assert probs[0] == x and probs[1] == y

