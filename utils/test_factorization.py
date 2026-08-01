
def test_factorization():
    A = randmatrix(5)
    P, L, U = lu(A)
    assert mnorm(P*A - L*U, 1) < 1.e-15

