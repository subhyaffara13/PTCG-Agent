
def test_action_verbs():
    assert nsimplify(1/(exp(3*pi*x/5) + 1)) == \
        (1/(exp(3*pi*x/5) + 1)).nsimplify()
    assert ratsimp(1/x + 1/y) == (1/x + 1/y).ratsimp()
    assert trigsimp(log(x), deep=True) == (log(x)).trigsimp(deep=True)
    assert radsimp(1/(2 + sqrt(2))) == (1/(2 + sqrt(2))).radsimp()
    assert radsimp(1/(a + b*sqrt(c)), symbolic=False) == \
        (1/(a + b*sqrt(c))).radsimp(symbolic=False)
    assert powsimp(x**y*x**z*y**z, combine='all') == \
        (x**y*x**z*y**z).powsimp(combine='all')
    assert (x**t*y**t).powsimp(force=True) == (x*y)**t
    assert simplify(x**y*x**z*y**z) == (x**y*x**z*y**z).simplify()
    assert together(1/x + 1/y) == (1/x + 1/y).together()
    assert collect(a*x**2 + b*x**2 + a*x - b*x + c, x) == \
        (a*x**2 + b*x**2 + a*x - b*x + c).collect(x)
    assert apart(y/(y + 2)/(y + 1), y) == (y/(y + 2)/(y + 1)).apart(y)
    assert combsimp(y/(x + 2)/(x + 1)) == (y/(x + 2)/(x + 1)).combsimp()
    assert gammasimp(gamma(x)/gamma(x-5)) == (gamma(x)/gamma(x-5)).gammasimp()
    assert factor(x**2 + 5*x + 6) == (x**2 + 5*x + 6).factor()
    assert refine(sqrt(x**2)) == sqrt(x**2).refine()
    assert cancel((x**2 + 5*x + 6)/(x + 2)) == ((x**2 + 5*x + 6)/(x + 2)).cancel()

