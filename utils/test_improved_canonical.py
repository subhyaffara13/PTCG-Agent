
def test_improved_canonical():
    def test_different_forms(listofforms):
        for form1, form2 in combinations(listofforms, 2):
            assert form1.canonical == form2.canonical

    def generate_forms(expr):
        return [expr, expr.reversed, expr.reversedsign,
                expr.reversed.reversedsign]

    test_different_forms(generate_forms(x > -y))
    test_different_forms(generate_forms(x >= -y))
    test_different_forms(generate_forms(Eq(x, -y)))
    test_different_forms(generate_forms(Ne(x, -y)))
    test_different_forms(generate_forms(pi < x))
    test_different_forms(generate_forms(pi - 5*y < -x + 2*y**2 - 7))

    assert (pi >= x).canonical == (x <= pi)

