
def test_rewrite2():
    e = exp(x)*log(log(exp(x)))
    assert mmrv(e, x) == {exp(x)}
    assert mrewrite(mrv(e, x), x, m) == (1/m*log(x), -x)

