
def test_issue_3740():
    f = 4*log(x) - 2*log(x)**2
    fid = diff(integrate(f, x), x)
    assert abs(f.subs(x, 42).evalf() - fid.subs(x, 42).evalf()) < 1e-10

