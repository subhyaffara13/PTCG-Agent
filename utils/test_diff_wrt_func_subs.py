
def test_diff_wrt_func_subs():
    assert f(g(x)).diff(x).subs(g, Lambda(x, 2*x)).doit() == f(2*x).diff(x)

