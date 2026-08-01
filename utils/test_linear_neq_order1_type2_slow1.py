
def test_linear_neq_order1_type2_slow1():
    i, r1, c1, r2, c2, t = symbols('i, r1, c1, r2, c2, t')
    x1 = Function('x1')
    x2 = Function('x2')

    eq1 = r1*c1*Derivative(x1(t), t) + x1(t) - x2(t) - r1*i
    eq2 = r2*c1*Derivative(x1(t), t) + r2*c2*Derivative(x2(t), t) + x2(t) - r2*i
    eq = [eq1, eq2]

    # XXX: Solution is too complicated
    [sol] = dsolve_system(eq, simplify=False, doit=False)
    assert checksysodesol(eq, sol) == (True, [0, 0])

