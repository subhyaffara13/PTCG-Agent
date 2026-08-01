
def riccati_reduced(eq, f, x):
    """
    Convert a Riccati ODE into its corresponding
    normal Riccati ODE.
    """
    match, funcs = match_riccati(eq, f, x)
    # If equation is not a Riccati ODE, exit
    if not match:
        return False
    # Using the rational functions, find the expression for a(x)
    b0, b1, b2 = funcs
    a = -b0*b2 + b1**2/4 - b1.diff(x)/2 + 3*b2.diff(x)**2/(4*b2**2) + b1*b2.diff(x)/(2*b2) - \
        b2.diff(x, 2)/(2*b2)
    # Normal form of Riccati ODE is f'(x) + f(x)^2 = a(x)
    return f(x).diff(x) + f(x)**2 - a

