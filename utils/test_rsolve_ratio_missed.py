
def test_rsolve_ratio_missed():
    # this arises during computation
    # assert rsolve_hyper([-1, 1], 3*(n + n**2), n).expand() == C0 + n**3 - n
    assert rsolve_ratio([-n, n + 2], n, n) is not None

