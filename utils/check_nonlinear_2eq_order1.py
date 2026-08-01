
def check_nonlinear_2eq_order1(eq, func, func_coef):
    t = list(list(eq[0].atoms(Derivative))[0].atoms(Symbol))[0]
    f = Wild('f')
    g = Wild('g')
    u, v = symbols('u, v', cls=Dummy)
    def check_type(x, y):
        r1 = eq[0].match(t*diff(x(t),t) - x(t) + f)
        r2 = eq[1].match(t*diff(y(t),t) - y(t) + g)
        if not (r1 and r2):
            r1 = eq[0].match(diff(x(t),t) - x(t)/t + f/t)
            r2 = eq[1].match(diff(y(t),t) - y(t)/t + g/t)
        if not (r1 and r2):
            r1 = (-eq[0]).match(t*diff(x(t),t) - x(t) + f)
            r2 = (-eq[1]).match(t*diff(y(t),t) - y(t) + g)
        if not (r1 and r2):
            r1 = (-eq[0]).match(diff(x(t),t) - x(t)/t + f/t)
            r2 = (-eq[1]).match(diff(y(t),t) - y(t)/t + g/t)
        if r1 and r2 and not (r1[f].subs(diff(x(t),t),u).subs(diff(y(t),t),v).has(t) \
        or r2[g].subs(diff(x(t),t),u).subs(diff(y(t),t),v).has(t)):
            return 'type5'
        else:
            return None
    for func_ in func:
        if isinstance(func_, list):
            x = func[0][0].func
            y = func[0][1].func
            eq_type = check_type(x, y)
            if not eq_type:
                eq_type = check_type(y, x)
            return eq_type
    x = func[0].func
    y = func[1].func
    fc = func_coef
    n = Wild('n', exclude=[x(t),y(t)])
    f1 = Wild('f1', exclude=[v,t])
    f2 = Wild('f2', exclude=[v,t])
    g1 = Wild('g1', exclude=[u,t])
    g2 = Wild('g2', exclude=[u,t])
    for i in range(2):
        eqs = 0
        for terms in Add.make_args(eq[i]):
            eqs += terms/fc[i,func[i],1]
        eq[i] = eqs
    r = eq[0].match(diff(x(t),t) - x(t)**n*f)
    if r:
        g = (diff(y(t),t) - eq[1])/r[f]
    if r and not (g.has(x(t)) or g.subs(y(t),v).has(t) or r[f].subs(x(t),u).subs(y(t),v).has(t)):
        return 'type1'
    r = eq[0].match(diff(x(t),t) - exp(n*x(t))*f)
    if r:
        g = (diff(y(t),t) - eq[1])/r[f]
    if r and not (g.has(x(t)) or g.subs(y(t),v).has(t) or r[f].subs(x(t),u).subs(y(t),v).has(t)):
        return 'type2'
    g = Wild('g')
    r1 = eq[0].match(diff(x(t),t) - f)
    r2 = eq[1].match(diff(y(t),t) - g)
    if r1 and r2 and not (r1[f].subs(x(t),u).subs(y(t),v).has(t) or \
    r2[g].subs(x(t),u).subs(y(t),v).has(t)):
        return 'type3'
    r1 = eq[0].match(diff(x(t),t) - f)
    r2 = eq[1].match(diff(y(t),t) - g)
    num, den = (
        (r1[f].subs(x(t),u).subs(y(t),v))/
        (r2[g].subs(x(t),u).subs(y(t),v))).as_numer_denom()
    R1 = num.match(f1*g1)
    R2 = den.match(f2*g2)
    # phi = (r1[f].subs(x(t),u).subs(y(t),v))/num
    if R1 and R2:
        return 'type4'
    return None

