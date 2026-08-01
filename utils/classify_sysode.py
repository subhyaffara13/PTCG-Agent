
def classify_sysode(eq, funcs=None, **kwargs):
    r"""
    Returns a dictionary of parameter names and values that define the system
    of ordinary differential equations in ``eq``.
    The parameters are further used in
    :py:meth:`~sympy.solvers.ode.dsolve` for solving that system.

    Some parameter names and values are:

    'is_linear' (boolean), which tells whether the given system is linear.
    Note that "linear" here refers to the operator: terms such as ``x*diff(x,t)`` are
    nonlinear, whereas terms like ``sin(t)*diff(x,t)`` are still linear operators.

    'func' (list) contains the :py:class:`~sympy.core.function.Function`s that
    appear with a derivative in the ODE, i.e. those that we are trying to solve
    the ODE for.

    'order' (dict) with the maximum derivative for each element of the 'func'
    parameter.

    'func_coeff' (dict or Matrix) with the coefficient for each triple ``(equation number,
    function, order)```. The coefficients are those subexpressions that do not
    appear in 'func', and hence can be considered constant for purposes of ODE
    solving. The value of this parameter can also be a  Matrix if the system of ODEs are
    linear first order of the form X' = AX where X is the vector of dependent variables.
    Here, this function returns the coefficient matrix A.

    'eq' (list) with the equations from ``eq``, sympified and transformed into
    expressions (we are solving for these expressions to be zero).

    'no_of_equations' (int) is the number of equations (same as ``len(eq)``).

    'type_of_equation' (string) is an internal classification of the type of
    ODE.

    'is_constant' (boolean), which tells if the system of ODEs is constant coefficient
    or not. This key is temporary addition for now and is in the match dict only when
    the system of ODEs is linear first order constant coefficient homogeneous. So, this
    key's value is True for now if it is available else it does not exist.

    'is_homogeneous' (boolean), which tells if the system of ODEs is homogeneous. Like the
    key 'is_constant', this key is a temporary addition and it is True since this key value
    is available only when the system is linear first order constant coefficient homogeneous.

    References
    ==========
    -https://eqworld.ipmnet.ru/en/solutions/sysode/sode-toc1.htm
    -A. D. Polyanin and A. V. Manzhirov, Handbook of Mathematics for Engineers and Scientists

    Examples
    ========

    >>> from sympy import Function, Eq, symbols, diff
    >>> from sympy.solvers.ode.ode import classify_sysode
    >>> from sympy.abc import t
    >>> f, x, y = symbols('f, x, y', cls=Function)
    >>> k, l, m, n = symbols('k, l, m, n', Integer=True)
    >>> x1 = diff(x(t), t) ; y1 = diff(y(t), t)
    >>> x2 = diff(x(t), t, t) ; y2 = diff(y(t), t, t)
    >>> eq = (Eq(x1, 12*x(t) - 6*y(t)), Eq(y1, 11*x(t) + 3*y(t)))
    >>> classify_sysode(eq)
    {'eq': [-12*x(t) + 6*y(t) + Derivative(x(t), t), -11*x(t) - 3*y(t) + Derivative(y(t), t)], 'func': [x(t), y(t)],
     'func_coeff': {(0, x(t), 0): -12, (0, x(t), 1): 1, (0, y(t), 0): 6, (0, y(t), 1): 0, (1, x(t), 0): -11, (1, x(t), 1): 0, (1, y(t), 0): -3, (1, y(t), 1): 1}, 'is_linear': True, 'no_of_equation': 2, 'order': {x(t): 1, y(t): 1}, 'type_of_equation': None}
    >>> eq = (Eq(diff(x(t),t), 5*t*x(t) + t**2*y(t) + 2), Eq(diff(y(t),t), -t**2*x(t) + 5*t*y(t)))
    >>> classify_sysode(eq)
    {'eq': [-t**2*y(t) - 5*t*x(t) + Derivative(x(t), t) - 2, t**2*x(t) - 5*t*y(t) + Derivative(y(t), t)],
     'func': [x(t), y(t)], 'func_coeff': {(0, x(t), 0): -5*t, (0, x(t), 1): 1, (0, y(t), 0): -t**2, (0, y(t), 1): 0,
     (1, x(t), 0): t**2, (1, x(t), 1): 0, (1, y(t), 0): -5*t, (1, y(t), 1): 1}, 'is_linear': True, 'no_of_equation': 2,
      'order': {x(t): 1, y(t): 1}, 'type_of_equation': None}

    """

    # Sympify equations and convert iterables of equations into
    # a list of equations
    def _sympify(eq):
        return list(map(sympify, eq if iterable(eq) else [eq]))

    eq, funcs = (_sympify(w) for w in [eq, funcs])
    for i, fi in enumerate(eq):
        if isinstance(fi, Equality):
            eq[i] = fi.lhs - fi.rhs

    t = list(list(eq[0].atoms(Derivative))[0].atoms(Symbol))[0]
    matching_hints = {"no_of_equation":i+1}
    matching_hints['eq'] = eq
    if i==0:
        raise ValueError("classify_sysode() works for systems of ODEs. "
        "For scalar ODEs, classify_ode should be used")

    # find all the functions if not given
    order = {}
    if funcs==[None]:
        funcs = _extract_funcs(eq)

    funcs = list(set(funcs))
    if len(funcs) != len(eq):
        raise ValueError("Number of functions given is not equal to the number of equations %s" % funcs)

    # This logic of list of lists in funcs to
    # be replaced later.
    func_dict = {}
    for func in funcs:
        if not order.get(func, False):
            max_order = 0
            for i, eqs_ in enumerate(eq):
                order_ = ode_order(eqs_,func)
                if max_order < order_:
                    max_order = order_
                    eq_no = i
            if eq_no in func_dict:
                func_dict[eq_no] = [func_dict[eq_no], func]
            else:
                func_dict[eq_no] = func
            order[func] = max_order

    funcs = [func_dict[i] for i in range(len(func_dict))]
    matching_hints['func'] = funcs
    for func in funcs:
        if isinstance(func, list):
            for func_elem in func:
                if len(func_elem.args) != 1:
                    raise ValueError("dsolve() and classify_sysode() work with "
                    "functions of one variable only, not %s" % func)
        else:
            if func and len(func.args) != 1:
                raise ValueError("dsolve() and classify_sysode() work with "
                "functions of one variable only, not %s" % func)

    # find the order of all equation in system of odes
    matching_hints["order"] = order

    # find coefficients of terms f(t), diff(f(t),t) and higher derivatives
    # and similarly for other functions g(t), diff(g(t),t) in all equations.
    # Here j denotes the equation number, funcs[l] denotes the function about
    # which we are talking about and k denotes the order of function funcs[l]
    # whose coefficient we are calculating.
    def linearity_check(eqs, j, func, is_linear_):
        for k in range(order[func] + 1):
            func_coef[j, func, k] = collect(eqs.expand(), [diff(func, t, k)]).coeff(diff(func, t, k))
            if is_linear_ == True:
                if func_coef[j, func, k] == 0:
                    if k == 0:
                        coef = eqs.as_independent(func, as_Add=True)[1]
                        for xr in range(1, ode_order(eqs,func) + 1):
                            coef -= eqs.as_independent(diff(func, t, xr), as_Add=True)[1]
                        if coef != 0:
                            is_linear_ = False
                    else:
                        if eqs.as_independent(diff(func, t, k), as_Add=True)[1]:
                            is_linear_ = False
                else:
                    for func_ in funcs:
                        if isinstance(func_, list):
                            for elem_func_ in func_:
                                dep = func_coef[j, func, k].as_independent(elem_func_, as_Add=True)[1]
                                if dep != 0:
                                    is_linear_ = False
                        else:
                            dep = func_coef[j, func, k].as_independent(func_, as_Add=True)[1]
                            if dep != 0:
                                is_linear_ = False
        return is_linear_

    func_coef = {}
    is_linear = True
    for j, eqs in enumerate(eq):
        for func in funcs:
            if isinstance(func, list):
                for func_elem in func:
                    is_linear = linearity_check(eqs, j, func_elem, is_linear)
            else:
                is_linear = linearity_check(eqs, j, func, is_linear)
    matching_hints['func_coeff'] = func_coef
    matching_hints['is_linear'] = is_linear


    if len(set(order.values())) == 1:
        order_eq = list(matching_hints['order'].values())[0]
        if matching_hints['is_linear'] == True:
            if matching_hints['no_of_equation'] == 2:
                if order_eq == 1:
                    type_of_equation = check_linear_2eq_order1(eq, funcs, func_coef)
                else:
                    type_of_equation = None
            # If the equation does not match up with any of the
            # general case solvers in systems.py and the number
            # of equations is greater than 2, then NotImplementedError
            # should be raised.
            else:
                type_of_equation = None

        else:
            if matching_hints['no_of_equation'] == 2:
                if order_eq == 1:
                    type_of_equation = check_nonlinear_2eq_order1(eq, funcs, func_coef)
                else:
                    type_of_equation = None
            elif matching_hints['no_of_equation'] == 3:
                if order_eq == 1:
                    type_of_equation = check_nonlinear_3eq_order1(eq, funcs, func_coef)
                else:
                    type_of_equation = None
            else:
                type_of_equation = None
    else:
        type_of_equation = None

    matching_hints['type_of_equation'] = type_of_equation

    return matching_hints

