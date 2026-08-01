
def sysode_linear_2eq_order1(match_):
    x = match_['func'][0].func
    y = match_['func'][1].func
    func = match_['func']
    fc = match_['func_coeff']
    eq = match_['eq']
    r = {}
    t = list(list(eq[0].atoms(Derivative))[0].atoms(Symbol))[0]
    for i in range(2):
        eq[i] = Add(*[terms/fc[i,func[i],1] for terms in Add.make_args(eq[i])])

    # for equations Eq(a1*diff(x(t),t), a*x(t) + b*y(t) + k1)
    # and Eq(a2*diff(x(t),t), c*x(t) + d*y(t) + k2)
    r['a'] = -fc[0,x(t),0]/fc[0,x(t),1]
    r['c'] = -fc[1,x(t),0]/fc[1,y(t),1]
    r['b'] = -fc[0,y(t),0]/fc[0,x(t),1]
    r['d'] = -fc[1,y(t),0]/fc[1,y(t),1]
    forcing = [S.Zero,S.Zero]
    for i in range(2):
        for j in Add.make_args(eq[i]):
            if not j.has(x(t), y(t)):
                forcing[i] += j
    if not (forcing[0].has(t) or forcing[1].has(t)):
        r['k1'] = forcing[0]
        r['k2'] = forcing[1]
    else:
        raise NotImplementedError("Only homogeneous problems are supported" +
                                  " (and constant inhomogeneity)")

    if match_['type_of_equation'] == 'type6':
        sol = _linear_2eq_order1_type6(x, y, t, r, eq)
    if match_['type_of_equation'] == 'type7':
        sol = _linear_2eq_order1_type7(x, y, t, r, eq)
    return sol

