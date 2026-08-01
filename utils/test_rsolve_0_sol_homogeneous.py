
def test_rsolve_0_sol_homogeneous():
    # fixed by cherry-pick from
    # https://github.com/diofant/diofant/commit/e1d2e52125199eb3df59f12e8944f8a5f24b00a5
    assert rsolve_hyper([n**2 - n + 12, 1], n*(n**2 - n + 12) + n + 1, n) == n

