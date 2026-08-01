
def test_issue_18203():
    eq = CRootOf(x**5 + 11*x - 2, 0) + CRootOf(x**5 + 11*x - 2, 1)
    assert cse(eq) == ([], [eq])

