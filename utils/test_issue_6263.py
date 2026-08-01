
def test_issue_6263():
    e = Eq(x*(-x + 1) + x*(x - 1), 0)
    assert cse(e, optimizations='basic') == ([], [True])

