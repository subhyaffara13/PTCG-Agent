
def test_issue_13000():
    eq = x/(-4*x**2 + y**2)
    cse_eq = cse(eq)[1][0]
    assert cse_eq == eq

