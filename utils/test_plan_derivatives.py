
def test_plan_derivatives():
    a1, a2, a3 = 1, 2, S('1/2')
    b1, b2 = 3, S('5/2')
    h = Hyper_Function((a1, a2, a3), (b1, b2))
    h2 = Hyper_Function((a1 + 1, a2 + 1, a3 + 2), (b1 + 1, b2 + 1))
    ops = devise_plan(h2, h, z)
    f = Formula(h, z, h(z), [])
    deriv = make_derivative_operator(f.M, z)
    assert tn((apply_operators(f.C, ops, deriv)*f.B)[0], h2(z), z)

    h2 = Hyper_Function((a1, a2 - 1, a3 - 2), (b1 - 1, b2 - 1))
    ops = devise_plan(h2, h, z)
    assert tn((apply_operators(f.C, ops, deriv)*f.B)[0], h2(z), z)

