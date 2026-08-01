
def sysode_nonlinear_2eq_order1(match_):
    func = match_['func']
    eq = match_['eq']
    fc = match_['func_coeff']
    t = list(list(eq[0].atoms(Derivative))[0].atoms(Symbol))[0]
    if match_['type_of_equation'] == 'type5':
        sol = _nonlinear_2eq_order1_type5(func, t, eq)
        return sol
    x = func[0].func
    y = func[1].func
    for i in range(2):
        eqs = 0
        for terms in Add.make_args(eq[i]):
            eqs += terms/fc[i,func[i],1]
        eq[i] = eqs
    if match_['type_of_equation'] == 'type1':
        sol = _nonlinear_2eq_order1_type1(x, y, t, eq)
    elif match_['type_of_equation'] == 'type2':
        sol = _nonlinear_2eq_order1_type2(x, y, t, eq)
    elif match_['type_of_equation'] == 'type3':
        sol = _nonlinear_2eq_order1_type3(x, y, t, eq)
    elif match_['type_of_equation'] == 'type4':
        sol = _nonlinear_2eq_order1_type4(x, y, t, eq)
    return sol

