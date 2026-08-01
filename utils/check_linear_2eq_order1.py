
def check_linear_2eq_order1(eq, func, func_coef):
    x = func[0].func
    y = func[1].func
    fc = func_coef
    t = list(list(eq[0].atoms(Derivative))[0].atoms(Symbol))[0]
    r = {}
    # for equations Eq(a1*diff(x(t),t), b1*x(t) + c1*y(t) + d1)
    # and Eq(a2*diff(y(t),t), b2*x(t) + c2*y(t) + d2)
    r['a1'] = fc[0,x(t),1] ; r['a2'] = fc[1,y(t),1]
    r['b1'] = -fc[0,x(t),0]/fc[0,x(t),1] ; r['b2'] = -fc[1,x(t),0]/fc[1,y(t),1]
    r['c1'] = -fc[0,y(t),0]/fc[0,x(t),1] ; r['c2'] = -fc[1,y(t),0]/fc[1,y(t),1]
    forcing = [S.Zero,S.Zero]
    for i in range(2):
        for j in Add.make_args(eq[i]):
            if not j.has(x(t), y(t)):
                forcing[i] += j
    if not (forcing[0].has(t) or forcing[1].has(t)):
        # We can handle homogeneous case and simple constant forcings
        r['d1'] = forcing[0]
        r['d2'] = forcing[1]
    else:
        # Issue #9244: nonhomogeneous linear systems are not supported
        return None

    # Conditions to check for type 6 whose equations are Eq(diff(x(t),t), f(t)*x(t) + g(t)*y(t)) and
    # Eq(diff(y(t),t), a*[f(t) + a*h(t)]x(t) + a*[g(t) - h(t)]*y(t))
    p = 0
    q = 0
    p1 = cancel(r['b2']/(cancel(r['b2']/r['c2']).as_numer_denom()[0]))
    p2 = cancel(r['b1']/(cancel(r['b1']/r['c1']).as_numer_denom()[0]))
    for n, i in enumerate([p1, p2]):
        for j in Mul.make_args(collect_const(i)):
            if not j.has(t):
                q = j
            if q and n==0:
                if ((r['b2']/j - r['b1'])/(r['c1'] - r['c2']/j)) == j:
                    p = 1
            elif q and n==1:
                if ((r['b1']/j - r['b2'])/(r['c2'] - r['c1']/j)) == j:
                    p = 2
    # End of condition for type 6

    if r['d1']!=0 or r['d2']!=0:
        return None
    else:
        if not any(r[k].has(t) for k in 'a1 a2 b1 b2 c1 c2'.split()):
            return None
        else:
            r['b1'] = r['b1']/r['a1'] ; r['b2'] = r['b2']/r['a2']
            r['c1'] = r['c1']/r['a1'] ; r['c2'] = r['c2']/r['a2']
            if p:
                return "type6"
            else:
                # Equations for type 7 are Eq(diff(x(t),t), f(t)*x(t) + g(t)*y(t)) and Eq(diff(y(t),t), h(t)*x(t) + p(t)*y(t))
                return "type7"

