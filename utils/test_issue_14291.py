
def test_issue_14291():
    assert Poly(((x - 1)**2 + 1)*((x - 1)**2 + 2)*(x - 1)
        ).all_roots() == [1, 1 - I, 1 + I, 1 - sqrt(2)*I, 1 + sqrt(2)*I]
    p = x**4 + 10*x**2 + 1
    ans = [rootof(p, i) for i in range(4)]
    assert Poly(p).all_roots() == ans
    _check(ans)

