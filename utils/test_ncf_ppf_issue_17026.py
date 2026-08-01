
def test_ncf_ppf_issue_17026():
    # Regression test for gh-17026
    x = np.linspace(0, 1, 600)
    x[0] = 1e-16
    par = (0.1, 2, 5, 0, 1)
    q = stats.ncf.ppf(x, *par)
    q0 = [stats.ncf.ppf(xi, *par) for xi in x]
    assert_allclose(q, q0)

