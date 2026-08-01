
def test_generate_A():
    # Data from DLMF 8.20.5
    x = sympy.symbols('x')
    Astd = [Poly(1, x),
            Poly(1, x),
            Poly(1 - 2*x),
            Poly(1 - 8*x + 6*x**2)]
    Ares = generate_A(len(Astd))

    for p, q in zip(Astd, Ares):
        assert_equal(p, q)

