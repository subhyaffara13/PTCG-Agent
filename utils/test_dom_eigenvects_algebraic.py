
def test_dom_eigenvects_algebraic():
    # Algebraic eigenvalues
    A = DomainMatrix([[QQ(1), QQ(2)], [QQ(3), QQ(4)]], (2, 2), QQ)
    Avects = dom_eigenvects(A)

    # Extract the dummy to build the expected result:
    lamda = Avects[1][0][1].gens[0]
    irreducible = Poly(lamda**2 - 5*lamda - 2, lamda, domain=QQ)
    K = FiniteExtension(irreducible)
    KK = K.from_sympy
    algebraic_eigenvects = [
        (K, irreducible, 1, DomainMatrix([[KK((lamda-4)/3), KK(1)]], (1, 2), K)),
    ]
    assert Avects == ([], algebraic_eigenvects)

    # Test converting to Expr:
    sympy_eigenvects = [
        (S(5)/2 - sqrt(33)/2, 1, [Matrix([[-sqrt(33)/6 - S(1)/2], [1]])]),
        (S(5)/2 + sqrt(33)/2, 1, [Matrix([[-S(1)/2 + sqrt(33)/6], [1]])]),
    ]
    assert dom_eigenvects_to_sympy([], algebraic_eigenvects, Matrix) == sympy_eigenvects

