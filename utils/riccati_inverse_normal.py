
def riccati_inverse_normal(y, x, b1, b2, bp=None):
    """
    Inverse transforming the solution to the normal
    Riccati ODE to get the solution to the Riccati ODE.
    """
    # bp is the expression which is independent of the solution
    # and hence, it need not be computed again
    if bp is None:
        bp = -b2.diff(x)/(2*b2**2) - b1/(2*b2)
    # w(x) = -y(x)/b2(x) - b2'(x)/(2*b2(x)^2) - b1(x)/(2*b2(x))
    return -y/b2 + bp

