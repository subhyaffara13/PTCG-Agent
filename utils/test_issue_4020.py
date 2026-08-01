
def test_issue_4020():
    assert cse(x**5 + x**4 + x**3 + x**2, optimizations='basic') \
        == ([(x0, x**2)], [x0*(x**3 + x + x0 + 1)])

