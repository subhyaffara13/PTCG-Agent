
def test_issue_22546():
    p1, p2 = symbols('p1, p2', positive=True)
    ref = powsimp(p1**z/p2**z)
    e = z + 1
    ans = ref.subs(z, e)
    assert ans.is_Pow
    assert powsimp(p1**e/p2**e) == ans
    i = symbols('i', integer=True)
    ref = powsimp(x**i/y**i)
    e = i + 1
    ans = ref.subs(i, e)
    assert ans.is_Pow
    assert powsimp(x**e/y**e) == ans

