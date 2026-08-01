
def compute_m_ybar(x, poles, choice, N):
    """
    Helper function to calculate -

    1. m - The degree bound for the polynomial
    solution that must be found for the auxiliary
    differential equation.

    2. ybar - Part of the solution which can be
    computed using the poles, c and d vectors.
    """
    ybar = 0
    m = Poly(choice[-1][-1], x, extension=True)

    # Calculate the first (nested) summation for ybar
    # as given in Step 9 of the Thesis (Pg 82)
    dybar = []
    for i, polei in enumerate(poles):
        for j, cij in enumerate(choice[i]):
            dybar.append(cij/(x - polei)**(j + 1))
        m -=Poly(choice[i][0], x, extension=True)  # can't accumulate Poly and use with Add
    ybar += Add(*dybar)

    # Calculate the second summation for ybar
    for i in range(N+1):
        ybar += choice[-1][i]*x**i
    return (m.expr, ybar)

