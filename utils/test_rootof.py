
def test_rootof():
    r1 = rootof(x**3 + x + 1, 0)
    r2 = rootof(x**3 + x + 1, 1)
    K1 = QQ.algebraic_field(r1)
    K2 = QQ.algebraic_field(r2)
    assert construct_domain([r1]) == (EX, [EX(r1)])
    assert construct_domain([r2]) == (EX, [EX(r2)])
    assert construct_domain([r1, r2]) == (EX, [EX(r1), EX(r2)])

    assert construct_domain([r1], extension=True) == (
            K1, [K1.from_sympy(r1)])
    assert construct_domain([r2], extension=True) == (
            K2, [K2.from_sympy(r2)])

