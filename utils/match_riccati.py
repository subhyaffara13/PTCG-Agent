
def match_riccati(eq, f, x):
    """
    A function that matches and returns the coefficients
    if an equation is a Riccati ODE

    Parameters
    ==========

    eq: Equation to be matched
    f: Dependent variable
    x: Independent variable

    Returns
    =======

    match: True if equation is a Riccati ODE, False otherwise
    funcs: [b0, b1, b2] if match is True, [] otherwise. Here,
    b0, b1 and b2 are rational functions which match the equation.
    """
    # Group terms based on f(x)
    if isinstance(eq, Eq):
        eq = eq.lhs - eq.rhs
    eq = eq.expand().collect(f(x))
    cf = eq.coeff(f(x).diff(x))

    # There must be an f(x).diff(x) term.
    # eq must be an Add object since we are using the expanded
    # equation and it must have atleast 2 terms (b2 != 0)
    if cf != 0 and isinstance(eq, Add):

        # Divide all coefficients by the coefficient of f(x).diff(x)
        # and add the terms again to get the same equation
        eq = Add(*((x/cf).cancel() for x in eq.args)).collect(f(x))

        # Match the equation with the pattern
        b1 = -eq.coeff(f(x))
        b2 = -eq.coeff(f(x)**2)
        b0 = (f(x).diff(x) - b1*f(x) - b2*f(x)**2 - eq).expand()
        funcs = [b0, b1, b2]

        # Check if coefficients are not symbols and floats
        if any(len(x.atoms(Symbol)) > 1 or len(x.atoms(Float)) for x in funcs):
            return False, []

        # If b_0(x) contains f(x), it is not a Riccati ODE
        if len(b0.atoms(f)) or not all((b2 != 0, b0.is_rational_function(x),
            b1.is_rational_function(x), b2.is_rational_function(x))):
            return False, []
        return True, funcs
    return False, []

