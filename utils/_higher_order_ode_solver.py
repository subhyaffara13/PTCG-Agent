
def _higher_order_ode_solver(match):
    eqs = match["eq"]
    funcs = match["func"]
    t = match["t"]
    sysorder = match['order']
    type = match.get('type_of_equation', "type0")

    is_second_order = match.get('is_second_order', False)
    is_transformed = match.get('is_transformed', False)
    is_euler = is_transformed and type == "type1"
    is_higher_order_type2 = is_transformed and type == "type2" and 'P' in match

    if is_second_order:
        new_eqs, new_funcs = _second_order_to_first_order(eqs, funcs, t,
                                                          A1=match.get("A1", None), A0=match.get("A0", None),
                                                          b=match.get("rhs", None), type=type,
                                                          t_=match.get("t_", None))
    else:
        new_eqs, new_funcs = _higher_order_to_first_order(eqs, sysorder, t, funcs=funcs,
                                                          type=type, J=match.get('J', None),
                                                          f_t=match.get('f(t)', None),
                                                          P=match.get('P', None), b=match.get('rhs', None))

    if is_transformed:
        t = match.get('t_', t)

    if not is_higher_order_type2:
        new_eqs = _select_equations(new_eqs, [f.diff(t) for f in new_funcs])

    sol = None

    # NotImplementedError may be raised when the system may be actually
    # solvable if it can be just divided into sub-systems
    try:
        if not is_higher_order_type2:
            sol = _strong_component_solver(new_eqs, new_funcs, t)
    except NotImplementedError:
        sol = None

    # Dividing the system only when it becomes essential
    if sol is None:
        try:
            sol = _component_solver(new_eqs, new_funcs, t)
        except NotImplementedError:
            sol = None

    if sol is None:
        return sol

    is_second_order_type2 = is_second_order and type == "type2"

    underscores = '__' if is_transformed else '_'

    sol = _select_equations(sol, funcs,
                            key=lambda x: Function(Dummy('{}{}0'.format(x.func.__name__, underscores)))(t))

    if match.get("is_transformed", False):
        if is_second_order_type2:
            g_t = match["g(t)"]
            tau = match["tau"]
            sol = [Eq(s.lhs, s.rhs.subs(t, tau) * g_t) for s in sol]
        elif is_euler:
            t = match['t']
            tau = match['t_']
            sol = [s.subs(tau, log(t)) for s in sol]
        elif is_higher_order_type2:
            P = match['P']
            sol_vector = P * Matrix([s.rhs for s in sol])
            sol = [Eq(f, s) for f, s in zip(funcs, sol_vector)]

    return sol

