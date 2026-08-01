
def test_noncommutativity_honoured():
    A, B = symbols("A B", commutative=False)
    M = symbols('M', integer=True, positive=True)
    p = Sum(A*B**n, (n, 1, M))
    assert p.doit() == A*Piecewise((M, Eq(B, 1)),
                                   ((B - B**(M + 1))*(1 - B)**(-1), True))

    p = Sum(B**n*A, (n, 1, M))
    assert p.doit() == Piecewise((M, Eq(B, 1)),
                                 ((B - B**(M + 1))*(1 - B)**(-1), True))*A

    p = Sum(B**n*A*B**n, (n, 1, M))
    assert p.doit() == p

