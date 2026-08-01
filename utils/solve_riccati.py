
def solve_riccati(fx, x, b0, b1, b2, gensol=False):
    """
    The main function that gives particular/general
    solutions to Riccati ODEs that have atleast 1
    rational particular solution.
    """
    # Step 1 : Convert to Normal Form
    a = -b0*b2 + b1**2/4 - b1.diff(x)/2 + 3*b2.diff(x)**2/(4*b2**2) + b1*b2.diff(x)/(2*b2) - \
        b2.diff(x, 2)/(2*b2)
    a_t = a.together()
    num, den = [Poly(e, x, extension=True) for e in a_t.as_numer_denom()]
    num, den = num.cancel(den, include=True)

    # Step 2
    presol = []

    # Step 3 : a(x) is 0
    if num == 0:
        presol.append(1/(x + Dummy('C1')))

    # Step 4 : a(x) is a non-zero constant
    elif x not in num.free_symbols.union(den.free_symbols):
        presol.extend([sqrt(a), -sqrt(a)])

    # Step 5 : Find poles and valuation at infinity
    poles = roots(den, x)
    poles, muls = list(poles.keys()), list(poles.values())
    val_inf = val_at_inf(num, den, x)

    if len(poles):
        # Check necessary conditions (outlined in the module docstring)
        if not check_necessary_conds(val_inf, muls):
            raise ValueError("Rational Solution doesn't exist")

        # Step 6
        # Construct c-vectors for each singular point
        c = construct_c(num, den, x, poles, muls)

        # Construct d vectors for each singular point
        d = construct_d(num, den, x, val_inf)

        # Step 7 : Iterate over all possible combinations and return solutions
        # For each possible combination, generate an array of 0's and 1's
        # where 0 means pick 1st choice and 1 means pick the second choice.

        # NOTE: We could exit from the loop if we find 3 particular solutions,
        # but it is not implemented here as -
        #   a. Finding 3 particular solutions is very rare. Most of the time,
        #      only 2 particular solutions are found.
        #   b. In case we exit after finding 3 particular solutions, it might
        #      happen that 1 or 2 of them are redundant solutions. So, instead of
        #      spending some more time in computing the particular solutions,
        #      we will end up computing the general solution from a single
        #      particular solution which is usually slower than computing the
        #      general solution from 2 or 3 particular solutions.
        c.append(d)
        choices = product(*c)
        for choice in choices:
            m, ybar = compute_m_ybar(x, poles, choice, -val_inf//2)
            numy, deny = [Poly(e, x, extension=True) for e in ybar.together().as_numer_denom()]
            # Step 10 : Check if a valid solution exists. If yes, also check
            # if m is a non-negative integer
            if m.is_nonnegative == True and m.is_integer == True:

                # Step 11 : Find polynomial solutions of degree m for the auxiliary equation
                psol, coeffs, exists = solve_aux_eq(num, den, numy, deny, x, m)

                # Step 12 : If valid polynomial solution exists, append solution.
                if exists:
                    # m == 0 case
                    if psol == 1 and coeffs == 0:
                        # p(x) = 1, so p'(x)/p(x) term need not be added
                        presol.append(ybar)
                    # m is a positive integer and there are valid coefficients
                    elif len(coeffs):
                        # Substitute the valid coefficients to get p(x)
                        psol = psol.xreplace(coeffs)
                        # y(x) = ybar(x) + p'(x)/p(x)
                        presol.append(ybar + psol.diff(x)/psol)

    # Remove redundant solutions from the list of existing solutions
    remove = set()
    for i in range(len(presol)):
        for j in range(i+1, len(presol)):
            rem = remove_redundant_sols(presol[i], presol[j], x)
            if rem is not None:
                remove.add(rem)
    sols = [x for x in presol if x not in remove]

    # Step 15 : Inverse transform the solutions of the equation in normal form
    bp = -b2.diff(x)/(2*b2**2) - b1/(2*b2)

    # If general solution is required, compute it from the particular solutions
    if gensol:
        sols = [get_gen_sol_from_part_sol(sols, a, x)]

    # Inverse transform the particular solutions
    presol = [Eq(fx, riccati_inverse_normal(y, x, b1, b2, bp).cancel(extension=True)) for y in sols]
    return presol

