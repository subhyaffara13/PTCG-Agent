
def _derivate_diff_eq(listofpoly, K):
    """
    Let a differential equation a0(x)y(x) + a1(x)y'(x) + ... = 0
    where a0, a1,... are polynomials or rational functions. The function
    returns b0, b1, b2... such that the differential equation
    b0(x)y(x) + b1(x)y'(x) +... = 0 is formed after differentiating the
    former equation.
    """

    sol = []
    a = len(listofpoly) - 1
    sol.append(DMFdiff(listofpoly[0], K))

    for i, j in enumerate(listofpoly[1:]):
        sol.append(DMFdiff(j, K) + listofpoly[i])

    sol.append(listofpoly[a])
    return sol

