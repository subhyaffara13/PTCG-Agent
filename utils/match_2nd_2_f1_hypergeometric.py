
def match_2nd_2F1_hypergeometric(I, k, sing_point, func):
    x = func.args[0]
    a = Wild("a")
    b = Wild("b")
    c = Wild("c")
    t = Wild("t")
    s = Wild("s")
    r = Wild("r")
    alpha = Wild("alpha")
    beta = Wild("beta")
    gamma = Wild("gamma")
    delta = Wild("delta")
    # I0 of the standard 2F1 equation.
    I0 = ((a-b+1)*(a-b-1)*x**2 + 2*((1-a-b)*c + 2*a*b)*x + c*(c-2))/(4*x**2*(x-1)**2)
    if sing_point != [0, 1]:
        # If singular point is [0, 1] then we have standard equation.
        eqs = []
        sing_eqs = [-beta/alpha, -delta/gamma, (delta-beta)/(alpha-gamma)]
        # making equations for the finding the mobius transformation
        for i in range(3):
            if i<len(sing_point):
                eqs.append(Eq(sing_eqs[i], sing_point[i]))
            else:
                eqs.append(Eq(1/sing_eqs[i], 0))
        # solving above equations for the mobius transformation
        _beta = -alpha*sing_point[0]
        _delta = -gamma*sing_point[1]
        _gamma = alpha
        if len(sing_point) == 3:
            _gamma = (_beta + sing_point[2]*alpha)/(sing_point[2] - sing_point[1])
        mob = (alpha*x + beta)/(gamma*x + delta)
        mob = mob.subs(beta, _beta)
        mob = mob.subs(delta, _delta)
        mob = mob.subs(gamma, _gamma)
        mob = cancel(mob)
        t = (beta - delta*x)/(gamma*x - alpha)
        t = cancel(((t.subs(beta, _beta)).subs(delta, _delta)).subs(gamma, _gamma))
    else:
        mob = x
        t = x

    # applying mobius transformation in I to make it into I0.
    I = I.subs(x, t)
    I = I*(t.diff(x))**2
    I = factor(I)
    dict_I = {x**2:0, x:0, 1:0}
    I0_num, I0_dem = I0.as_numer_denom()
    # collecting coeff of (x**2, x), of the standard equation.
    # substituting (a-b) = s, (a+b) = r
    dict_I0 = {x**2:s**2 - 1, x:(2*(1-r)*c + (r+s)*(r-s)), 1:c*(c-2)}
    # collecting coeff of (x**2, x) from I0 of the given equation.
    dict_I.update(collect(expand(cancel(I*I0_dem)), [x**2, x], evaluate=False))
    eqs = []
    # We are comparing the coeff of powers of different x, for finding the values of
    # parameters of standard equation.
    for key in [x**2, x, 1]:
        eqs.append(Eq(dict_I[key], dict_I0[key]))

    # We can have many possible roots for the equation.
    # I am selecting the root on the basis that when we have
    # standard equation eq = x*(x-1)*f(x).diff(x, 2) + ((a+b+1)*x-c)*f(x).diff(x) + a*b*f(x)
    # then root should be a, b, c.

    _c = 1 - factor(sqrt(1+eqs[2].lhs))
    if not _c.has(Symbol):
        _c = min(list(roots(eqs[2], c)))
    _s = factor(sqrt(eqs[0].lhs + 1))
    _r = _c - factor(sqrt(_c**2 + _s**2 + eqs[1].lhs - 2*_c))
    _a = (_r + _s)/2
    _b = (_r - _s)/2

    rn = {'a':simplify(_a), 'b':simplify(_b), 'c':simplify(_c), 'k':k, 'mobius':mob, 'type':"2F1"}
    return rn

