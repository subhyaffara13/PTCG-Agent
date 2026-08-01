
def test_issue_22606():
    fx = Function('f')(x)
    eq = x + gamma(y)
    # seems like ans should be `eq`, not `(x*y + gamma(y + 1))/y`
    ans = gammasimp(eq)
    assert gammasimp(eq.subs(x, fx)).subs(fx, x) == ans
    assert gammasimp(eq.subs(x, cos(x))).subs(cos(x), x) == ans
    assert 1/gammasimp(1/eq) == ans
    assert gammasimp(fx.subs(x, eq)).args[0] == ans

