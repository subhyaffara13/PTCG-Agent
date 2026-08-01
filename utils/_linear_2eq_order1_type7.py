
def _linear_2eq_order1_type7(x, y, t, r, eq):
    r"""
    The equations of this type of ode are .

    .. math:: x' = f(t) x + g(t) y

    .. math:: y' = h(t) x + p(t) y

    Differentiating the first equation and substituting the value of `y`
    from second equation will give a second-order linear equation

    .. math:: g x'' - (fg + gp + g') x' + (fgp - g^{2} h + f g' - f' g) x = 0

    This above equation can be easily integrated if following conditions are satisfied.

    1. `fgp - g^{2} h + f g' - f' g = 0`

    2. `fgp - g^{2} h + f g' - f' g = ag, fg + gp + g' = bg`

    If first condition is satisfied then it is solved by current dsolve solver and in second case it becomes
    a constant coefficient differential equation which is also solved by current solver.

    Otherwise if the above condition fails then,
    a particular solution is assumed as `x = x_0(t)` and `y = y_0(t)`
    Then the general solution is expressed as

    .. math:: x = C_1 x_0(t) + C_2 x_0(t) \int \frac{g(t) F(t) P(t)}{x_0^{2}(t)} \,dt

    .. math:: y = C_1 y_0(t) + C_2 [\frac{F(t) P(t)}{x_0(t)} + y_0(t) \int \frac{g(t) F(t) P(t)}{x_0^{2}(t)} \,dt]

    where C1 and C2 are arbitrary constants and

    .. math:: F(t) = e^{\int f(t) \,dt}, P(t) = e^{\int p(t) \,dt}

    """
    C1, C2, C3, C4 = get_numbered_constants(eq, num=4)
    e1 = r['a']*r['b']*r['c'] - r['b']**2*r['c'] + r['a']*diff(r['b'],t) - diff(r['a'],t)*r['b']
    e2 = r['a']*r['c']*r['d'] - r['b']*r['c']**2 + diff(r['c'],t)*r['d'] - r['c']*diff(r['d'],t)
    m1 = r['a']*r['b'] + r['b']*r['d'] + diff(r['b'],t)
    m2 = r['a']*r['c'] + r['c']*r['d'] + diff(r['c'],t)
    if e1 == 0:
        sol1 = dsolve(r['b']*diff(x(t),t,t) - m1*diff(x(t),t)).rhs
        sol2 = dsolve(diff(y(t),t) - r['c']*sol1 - r['d']*y(t)).rhs
    elif e2 == 0:
        sol2 = dsolve(r['c']*diff(y(t),t,t) - m2*diff(y(t),t)).rhs
        sol1 = dsolve(diff(x(t),t) - r['a']*x(t) - r['b']*sol2).rhs
    elif not (e1/r['b']).has(t) and not (m1/r['b']).has(t):
        sol1 = dsolve(diff(x(t),t,t) - (m1/r['b'])*diff(x(t),t) - (e1/r['b'])*x(t)).rhs
        sol2 = dsolve(diff(y(t),t) - r['c']*sol1 - r['d']*y(t)).rhs
    elif not (e2/r['c']).has(t) and not (m2/r['c']).has(t):
        sol2 = dsolve(diff(y(t),t,t) - (m2/r['c'])*diff(y(t),t) - (e2/r['c'])*y(t)).rhs
        sol1 = dsolve(diff(x(t),t) - r['a']*x(t) - r['b']*sol2).rhs
    else:
        x0 = Function('x0')(t)    # x0 and y0 being particular solutions
        y0 = Function('y0')(t)
        F = exp(Integral(r['a'],t))
        P = exp(Integral(r['d'],t))
        sol1 = C1*x0 + C2*x0*Integral(r['b']*F*P/x0**2, t)
        sol2 = C1*y0 + C2*(F*P/x0 + y0*Integral(r['b']*F*P/x0**2, t))
    return [Eq(x(t), sol1), Eq(y(t), sol2)]

