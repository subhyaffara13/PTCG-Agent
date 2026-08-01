
def _remove_redundant_solutions(eq, solns, order, var):
    r"""
    Remove redundant solutions from the set of solutions.

    This function is needed because otherwise dsolve can return
    redundant solutions. As an example consider:

        eq = Eq((f(x).diff(x, 2))*f(x).diff(x), 0)

    There are two ways to find solutions to eq. The first is to solve f(x).diff(x, 2) = 0
    leading to solution f(x)=C1 + C2*x. The second is to solve the equation f(x).diff(x) = 0
    leading to the solution f(x) = C1. In this particular case we then see
    that the second solution is a special case of the first and we do not
    want to return it.

    This does not always happen. If we have

        eq = Eq((f(x)**2-4)*(f(x).diff(x)-4), 0)

    then we get the algebraic solution f(x) = [-2, 2] and the integral solution
    f(x) = x + C1 and in this case the two solutions are not equivalent wrt
    initial conditions so both should be returned.
    """
    def is_special_case_of(soln1, soln2):
        return _is_special_case_of(soln1, soln2, eq, order, var)

    unique_solns = []
    for soln1 in solns:
        for soln2 in unique_solns.copy():
            if is_special_case_of(soln1, soln2):
                break
            elif is_special_case_of(soln2, soln1):
                unique_solns.remove(soln2)
        else:
            unique_solns.append(soln1)

    return unique_solns

