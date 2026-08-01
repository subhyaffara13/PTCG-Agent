
def _higher_order_to_first_order(eqs, sys_order, t, funcs=None, type="type0", **kwargs):
    if funcs is None:
        funcs = sys_order.keys()

    # Standard Cauchy Euler system
    if type == "type1":
        t_ = Symbol('{}_'.format(t))
        new_funcs = [Function(Dummy('{}_'.format(f.func.__name__)))(t_) for f in funcs]
        max_order = max(sys_order[func] for func in funcs)
        subs_dict = dict(zip(funcs, new_funcs))
        subs_dict[t] = exp(t_)

        free_function = Function(Dummy())

        def _get_coeffs_from_subs_expression(expr):
            if isinstance(expr, Subs):
                free_symbol = expr.args[1][0]
                term = expr.args[0]
                return {ode_order(term, free_symbol): 1}

            if isinstance(expr, Mul):
                coeff = expr.args[0]
                order = list(_get_coeffs_from_subs_expression(expr.args[1]).keys())[0]
                return {order: coeff}

            if isinstance(expr, Add):
                coeffs = {}
                for arg in expr.args:

                    if isinstance(arg, Mul):
                        coeffs.update(_get_coeffs_from_subs_expression(arg))

                    else:
                        order = list(_get_coeffs_from_subs_expression(arg).keys())[0]
                        coeffs[order] = 1

                return coeffs

        for o in range(1, max_order + 1):
            expr = free_function(log(t_)).diff(t_, o)*t_**o
            coeff_dict = _get_coeffs_from_subs_expression(expr)
            coeffs = [coeff_dict[order] if order in coeff_dict else 0 for order in range(o + 1)]
            expr_to_subs = sum(free_function(t_).diff(t_, i) * c for i, c in
                        enumerate(coeffs)) / t**o
            subs_dict.update({f.diff(t, o): expr_to_subs.subs(free_function(t_), nf)
                              for f, nf in zip(funcs, new_funcs)})

        new_eqs = [eq.subs(subs_dict) for eq in eqs]
        new_sys_order = {nf: sys_order[f] for f, nf in zip(funcs, new_funcs)}

        new_eqs = canonical_odes(new_eqs, new_funcs, t_)[0]

        return _higher_order_to_first_order(new_eqs, new_sys_order, t_, funcs=new_funcs)

    # Systems of the form: X(n)(t) = f(t)*A*X + b
    # where X(n)(t) is the nth derivative of the vector of dependent variables
    # with respect to the independent variable and A is a constant matrix.
    if type == "type2":
        J = kwargs.get('J', None)
        f_t = kwargs.get('f_t', None)
        b = kwargs.get('b', None)
        P = kwargs.get('P', None)
        max_order = max(sys_order[func] for func in funcs)

        return _higher_order_type2_to_sub_systems(J, f_t, funcs, t, max_order, P=P, b=b)

        # Note: To be changed to this after doit option is disabled for default cases
        # new_sysorder = _get_func_order(new_eqs, new_funcs)
        #
        # return _higher_order_to_first_order(new_eqs, new_sysorder, t, funcs=new_funcs)

    new_funcs = []

    for prev_func in funcs:
        func_name = prev_func.func.__name__
        func = Function(Dummy('{}_0'.format(func_name)))(t)
        new_funcs.append(func)
        subs_dict = {prev_func: func}
        new_eqs = []

        for i in range(1, sys_order[prev_func]):
            new_func = Function(Dummy('{}_{}'.format(func_name, i)))(t)
            subs_dict[prev_func.diff(t, i)] = new_func
            new_funcs.append(new_func)

            prev_f = subs_dict[prev_func.diff(t, i-1)]
            new_eq = Eq(prev_f.diff(t), new_func)
            new_eqs.append(new_eq)

        eqs = [eq.subs(subs_dict) for eq in eqs] + new_eqs

    return eqs, new_funcs

