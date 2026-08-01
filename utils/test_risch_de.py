
def test_rischDE():
    # TODO: Add more tests for rischDE, including ones from the text
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t, t)]})
    DE.decrement_level()
    assert rischDE(Poly(-2*x, x), Poly(1, x), Poly(1 - 2*x - 2*x**2, x),
    Poly(1, x), DE) == \
        (Poly(x + 1, x), Poly(1, x))

