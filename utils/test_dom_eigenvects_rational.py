
def test_dom_eigenvects_rational():
    # Rational eigenvalues
    A = DomainMatrix([[QQ(1), QQ(2)], [QQ(1), QQ(2)]], (2, 2), QQ)
    rational_eigenvects = [
        (QQ, QQ(3), 1, DomainMatrix([[QQ(1), QQ(1)]], (1, 2), QQ)),
        (QQ, QQ(0), 1, DomainMatrix([[QQ(-2), QQ(1)]], (1, 2), QQ)),
    ]
    assert dom_eigenvects(A) == (rational_eigenvects, [])

    # Test converting to Expr:
    sympy_eigenvects = [
        (S(3), 1, [Matrix([1, 1])]),
        (S(0), 1, [Matrix([-2, 1])]),
    ]
    assert dom_eigenvects_to_sympy(rational_eigenvects, [], Matrix) == sympy_eigenvects

