
def _linear_ode_solver(match):
    t = match['t']
    funcs = match['func']

    rhs = match.get('rhs', None)
    tau = match.get('tau', None)
    t = match['t_'] if 't_' in match else t
    A = match['func_coeff']

    # Note: To make B None when the matrix has constant
    # coefficient
    B = match.get('commutative_antiderivative', None)
    type = match['type_of_equation']

    sol_vector = linodesolve(A, t, b=rhs, B=B,
                             type=type, tau=tau)

    sol = [Eq(f, s) for f, s in zip(funcs, sol_vector)]

    return sol

