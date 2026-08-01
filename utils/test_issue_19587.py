
def test_issue_19587():
    n,m = symbols('n m')
    assert nonlinsolve([32*2**m*2**n - 4**n, 27*3**m - 3**(-n)], m, n) ==\
        FiniteSet((-log(81)/log(3), 1))

