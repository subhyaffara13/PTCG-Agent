
def test_nonlinear_3eq_order1():
    x, y, z = symbols('x, y, z', cls=Function)
    t, u = symbols('t u')
    eq1 = (4*diff(x(t),t) + 2*y(t)*z(t), 3*diff(y(t),t) - z(t)*x(t), 5*diff(z(t),t) - x(t)*y(t))
    sol1 = [Eq(4*Integral(1/(sqrt(-4*u**2 - 3*C1 + C2)*sqrt(-4*u**2 + 5*C1 - C2)), (u, x(t))),
        C3 - sqrt(15)*t/15), Eq(3*Integral(1/(sqrt(-6*u**2 - C1 + 5*C2)*sqrt(3*u**2 + C1 - 4*C2)),
        (u, y(t))), C3 + sqrt(5)*t/10), Eq(5*Integral(1/(sqrt(-10*u**2 - 3*C1 + C2)*
        sqrt(5*u**2 + 4*C1 - C2)), (u, z(t))), C3 + sqrt(3)*t/6)]
    assert [i.dummy_eq(j) for i, j in zip(dsolve(eq1), sol1)]
    # FIXME: assert checksysodesol(eq1, sol1) == (True, [0, 0, 0])

    eq2 = (4*diff(x(t),t) + 2*y(t)*z(t)*sin(t), 3*diff(y(t),t) - z(t)*x(t)*sin(t), 5*diff(z(t),t) - x(t)*y(t)*sin(t))
    sol2 = [Eq(3*Integral(1/(sqrt(-6*u**2 - C1 + 5*C2)*sqrt(3*u**2 + C1 - 4*C2)), (u, x(t))), C3 +
        sqrt(5)*cos(t)/10), Eq(4*Integral(1/(sqrt(-4*u**2 - 3*C1 + C2)*sqrt(-4*u**2 + 5*C1 - C2)),
        (u, y(t))), C3 - sqrt(15)*cos(t)/15), Eq(5*Integral(1/(sqrt(-10*u**2 - 3*C1 + C2)*
        sqrt(5*u**2 + 4*C1 - C2)), (u, z(t))), C3 + sqrt(3)*cos(t)/6)]
    assert [i.dummy_eq(j) for i, j in zip(dsolve(eq2), sol2)]

