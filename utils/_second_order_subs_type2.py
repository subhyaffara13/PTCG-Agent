
def _second_order_subs_type2(A, funcs, t_):
    r"""
    Returns a second order system based on the coefficient matrix passed.

    Explanation
    ===========

    This function returns a system of second order ODE of the following form:

    .. math::
        X'' = A * X

    Here, $X$ is the vector of dependent variables, but a bit modified, $A$ is the
    coefficient matrix passed.

    Along with returning the second order system, this function also returns the new
    dependent variables with the new independent variable `t_` passed.

    Parameters
    ==========

    A: Matrix
        Coefficient matrix of the system
    funcs: List
        List of old dependent variables
    t_: Symbol
        New independent variable

    Returns
    =======

    List, List

    """
    func_names = [func.func.__name__ for func in funcs]
    new_funcs = [Function(Dummy("{}_".format(name)))(t_) for name in func_names]
    rhss = A * Matrix(new_funcs)
    new_eqs = [Eq(func.diff(t_, 2), rhs) for func, rhs in zip(new_funcs, rhss)]

    return new_eqs, new_funcs

