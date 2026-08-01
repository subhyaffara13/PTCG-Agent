
def test_linear_3eq_order1_type4_slow():
    x, y, z = symbols('x, y, z', cls=Function)
    t = Symbol('t')

    f = t ** 3 + log(t)
    g = t ** 2 + sin(t)
    eq1 = (Eq(diff(x(t), t), (4 * f + g) * x(t) - f * y(t) - 2 * f * z(t)),
                Eq(diff(y(t), t), 2 * f * x(t) + (f + g) * y(t) - 2 * f * z(t)), Eq(diff(z(t), t), 5 * f * x(t) + f * y(
        t) + (-3 * f + g) * z(t)))
    with dotprodsimp(True):
        dsolve(eq1)

