
def _nonlinear_3eq_order1_type5(x, y, z, t, eq):
    r"""
    .. math:: x' = x (c F_2 - b F_3), \enspace y' = y (a F_3 - c F_1), \enspace z' = z (b F_1 - a F_2)

    where `F_n = F_n (x, y, z, t)` and are arbitrary functions.

    First Integral:

    .. math:: \left|x\right|^{a} \left|y\right|^{b} \left|z\right|^{c} = C_1

    where `C` is an arbitrary constant. If the function `F_n` is independent of `t`,
    then, by eliminating `t` and `z` from the first two equations of the system, one
    arrives at a first-order equation.

    References
    ==========
    -https://eqworld.ipmnet.ru/en/solutions/sysode/sode0406.pdf

    """
    C1 = get_numbered_constants(eq, num=1)
    u, v, w = symbols('u, v, w')
    fu, fv, fw = symbols('u, v, w', cls=Function)
    p = Wild('p', exclude=[x(t), y(t), z(t), t])
    q = Wild('q', exclude=[x(t), y(t), z(t), t])
    s = Wild('s', exclude=[x(t), y(t), z(t), t])
    F1, F2, F3 = symbols('F1, F2, F3', cls=Wild)
    r1 = eq[0].match(diff(x(t), t) - x(t)*F2 + x(t)*F3)
    r = collect_const(r1[F2]).match(s*F2)
    r.update(collect_const(r1[F3]).match(q*F3))
    if eq[1].has(r[F2]) and not eq[1].has(r[F3]):
        r[F2], r[F3] = r[F3], r[F2]
        r[s], r[q] = -r[q], -r[s]
    r.update((diff(y(t), t) - eq[1]).match(y(t)*(p*r[F3] - r[s]*F1)))
    a = r[p]; b = r[q]; c = r[s]
    F1 = r[F1].subs(x(t), u).subs(y(t), v).subs(z(t), w)
    F2 = r[F2].subs(x(t), u).subs(y(t), v).subs(z(t), w)
    F3 = r[F3].subs(x(t), u).subs(y(t), v).subs(z(t), w)
    x_yz = (C1*v**-b*w**-c)**-a
    y_zx = (C1*w**-c*u**-a)**-b
    z_xy = (C1*u**-a*v**-b)**-c
    y_x = dsolve(diff(fv(u), u) - ((v*(a*F3 - c*F1))/(u*(c*F2 - b*F3))).subs(w, z_xy).subs(v, fv(u))).rhs
    z_x = dsolve(diff(fw(u), u) - ((w*(b*F1 - a*F2))/(u*(c*F2 - b*F3))).subs(v, y_zx).subs(w, fw(u))).rhs
    z_y = dsolve(diff(fw(v), v) - ((w*(b*F1 - a*F2))/(v*(a*F3 - c*F1))).subs(u, x_yz).subs(w, fw(v))).rhs
    x_y = dsolve(diff(fu(v), v) - ((u*(c*F2 - b*F3))/(v*(a*F3 - c*F1))).subs(w, z_xy).subs(u, fu(v))).rhs
    y_z = dsolve(diff(fv(w), w) - ((v*(a*F3 - c*F1))/(w*(b*F1 - a*F2))).subs(u, x_yz).subs(v, fv(w))).rhs
    x_z = dsolve(diff(fu(w), w) - ((u*(c*F2 - b*F3))/(w*(b*F1 - a*F2))).subs(v, y_zx).subs(u, fu(w))).rhs
    sol1 = dsolve(diff(fu(t), t) - (u*(c*F2 - b*F3)).subs(v, y_x).subs(w, z_x).subs(u, fu(t))).rhs
    sol2 = dsolve(diff(fv(t), t) - (v*(a*F3 - c*F1)).subs(u, x_y).subs(w, z_y).subs(v, fv(t))).rhs
    sol3 = dsolve(diff(fw(t), t) - (w*(b*F1 - a*F2)).subs(u, x_z).subs(v, y_z).subs(w, fw(t))).rhs
    return [sol1, sol2, sol3]

