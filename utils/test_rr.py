
def test_RR():
    rs_funcs = [rs_sin, rs_cos, rs_tan, rs_cot, rs_atan, rs_tanh]
    sympy_funcs = [sin, cos, tan, cot, atan, tanh]
    R, x, y = ring('x, y', RR)
    a = symbols('a')
    for rs_func, sympy_func in zip(rs_funcs, sympy_funcs):
        p = rs_func(2 + x, x, 5).compose(x, 5)
        q = sympy_func(2 + a).series(a, 0, 5).removeO()
        is_close(p.as_expr(), q.subs(a, 5).n())

    p = rs_nth_root(2 + x, 5, x, 5).compose(x, 5)
    q = ((2 + a)**QQ(1, 5)).series(a, 0, 5).removeO()
    is_close(p.as_expr(), q.subs(a, 5).n())


def test_RR():
    # Make sure the algorithm does the right thing if the ring is RR. See
    # issue 8685.
    assert heurisch(sqrt(1 + 0.25*x**2), x, hints=[]) == \
        0.5*x*sqrt(0.25*x**2 + 1) + 1.0*asinh(0.5*x)

