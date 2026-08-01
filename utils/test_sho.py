
def test_sho():
    n, m = symbols('n,m')
    h_n = Bd(n)*B(n)*(n + S.Half)
    H = Sum(h_n, (n, 0, 5))
    o = H.doit(deep=False)
    b = FixedBosonicBasis(2, 6)
    m = matrix_rep(o, b)
    # We need to double check these energy values to make sure that they
    # are correct and have the proper degeneracies!
    diag = [1, 2, 3, 3, 4, 5, 4, 5, 6, 7, 5, 6, 7, 8, 9, 6, 7, 8, 9, 10, 11]
    for i in range(len(diag)):
        assert diag[i] == m[i, i]

