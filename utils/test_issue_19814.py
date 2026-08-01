
def test_issue_19814():
    assert nonlinsolve([ 2**m - 2**(2*n), 4*2**m - 2**(4*n)], m, n
                      ) == FiniteSet((log(2**(2*n))/log(2), S.Complexes))

