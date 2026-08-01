
def test_probs():
    d = Density([Ket(0), .75], [Ket(1), 0.25])
    probs = d.probs()
    assert probs[0] == 0.75 and probs[1] == 0.25

    #probs can be symbols
    x, y = symbols('x y')
    d = Density([Ket(0), x], [Ket(1), y])
    probs = d.probs()
    assert probs[0] == x and probs[1] == y

