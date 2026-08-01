
def test_issue_6360():
    a, b = symbols("a b")
    apb = a + b
    eq = apb + apb**2*(-2*a - 2*b)
    assert factor_terms(sub_pre(eq)) == a + b - 2*(a + b)**3

