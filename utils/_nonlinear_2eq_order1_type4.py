
def _nonlinear_2eq_order1_type4(x, y, t, eq):
    r"""
    Equation:

    .. math:: x' = f_1(x) g_1(y) \phi(x,y,t)

    .. math:: y' = f_2(x) g_2(y) \phi(x,y,t)

    First integral:

    .. math:: \int \frac{f_2(x)}{f_1(x)} \,dx - \int \frac{g_1(y)}{g_2(y)} \,dy = C

    where `C` is an arbitrary constant.

    On solving the first integral for `x` (resp., `y` ) and on substituting the
    resulting expression into either equation of the original solution, one
    arrives at a first-order equation for determining `y` (resp., `x` ).

    """
    C1, C2 = get_numbered_constants(eq, num=2)
    u, v = symbols('u, v')
    U, V = symbols('U, V', cls=Function)
    f = Wild('f')
    g = Wild('g')
    f1 = Wild('f1', exclude=[v,t])
    f2 = Wild('f2', exclude=[v,t])
    g1 = Wild('g1', exclude=[u,t])
    g2 = Wild('g2', exclude=[u,t])
    r1 = eq[0].match(diff(x(t),t) - f)
    r2 = eq[1].match(diff(y(t),t) - g)
    num, den = (
        (r1[f].subs(x(t),u).subs(y(t),v))/
        (r2[g].subs(x(t),u).subs(y(t),v))).as_numer_denom()
    R1 = num.match(f1*g1)
    R2 = den.match(f2*g2)
    phi = (r1[f].subs(x(t),u).subs(y(t),v))/num
    F1 = R1[f1]; F2 = R2[f2]
    G1 = R1[g1]; G2 = R2[g2]
    sol1r = solve(Integral(F2/F1, u).doit() - Integral(G1/G2,v).doit() - C1, u)
    sol2r = solve(Integral(F2/F1, u).doit() - Integral(G1/G2,v).doit() - C1, v)
    sol = []
    for sols in sol1r:
        sol.append(Eq(y(t), dsolve(diff(V(t),t) - F2.subs(u,sols).subs(v,V(t))*G2.subs(v,V(t))*phi.subs(u,sols).subs(v,V(t))).rhs))
    for sols in sol2r:
        sol.append(Eq(x(t), dsolve(diff(U(t),t) - F1.subs(u,U(t))*G1.subs(v,sols).subs(u,U(t))*phi.subs(v,sols).subs(u,U(t))).rhs))
    return set(sol)

