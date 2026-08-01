
def _second_order_to_first_order(eqs, funcs, t, type="auto", A1=None,
                                 A0=None, b=None, t_=None):
    r"""
    Expects the system to be in second order and in canonical form

    Explanation
    ===========

    Reduces a second order system into a first order one depending on the type of second
    order system.
    1. "type0": If this is passed, then the system will be reduced to first order by
                introducing dummy variables.
    2. "type1": If this is passed, then a particular substitution will be used to reduce the
                the system into first order.
    3. "type2": If this is passed, then the system will be transformed with new dependent
                variables and independent variables. This transformation is a part of solving
                the corresponding system of ODEs.

    `A1` and `A0` are the coefficient matrices from the system and it is assumed that the
    second order system has the form given below:

    .. math::
        A2 * X'' = A1 * X' + A0 * X + b

    Here, $A2$ is the coefficient matrix for the vector $X''$ and $b$ is the non-homogeneous
    term.

    Default value for `b` is None but if `A1` and `A0` are passed and `b` is not passed, then the
    system will be assumed homogeneous.

    """
    is_a1 = A1 is None
    is_a0 = A0 is None

    if (type == "type1" and is_a1) or (type == "type2" and is_a0)\
        or (type == "auto" and (is_a1 or is_a0)):
        (A2, A1, A0), b = linear_ode_to_matrix(eqs, funcs, t, 2)

        if not A2.is_Identity:
            raise ValueError(filldedent('''
                The system must be in its canonical form.
            '''))

    if type == "auto":
        match = _match_second_order_type(A1, A0, t)
        type = match["type_of_equation"]
        A1 = match.get("A1", None)
        A0 = match.get("A0", None)

    sys_order = dict.fromkeys(funcs, 2)

    if type == "type1":
        if b is None:
            b = zeros(len(eqs))
        eqs = _second_order_subs_type1(A1, b, funcs, t)
        sys_order = dict.fromkeys(funcs, 1)

    if type == "type2":
        if t_ is None:
            t_ = Symbol("{}_".format(t))
        t = t_
        eqs, funcs = _second_order_subs_type2(A0, funcs, t_)
        sys_order = dict.fromkeys(funcs, 2)

    return _higher_order_to_first_order(eqs, sys_order, t, funcs=funcs)

