
def remove_redundant_sols(sol1, sol2, x):
    """
    Helper function to remove redundant
    solutions to the differential equation.
    """
    # If y1 and y2 are redundant solutions, there is
    # some value of the arbitrary constant for which
    # they will be equal

    syms1 = sol1.atoms(Symbol, Dummy)
    syms2 = sol2.atoms(Symbol, Dummy)
    num1, den1 = [Poly(e, x, extension=True) for e in sol1.together().as_numer_denom()]
    num2, den2 = [Poly(e, x, extension=True) for e in sol2.together().as_numer_denom()]
    # Cross multiply
    e = num1*den2 - den1*num2
    # Check if there are any constants
    syms = list(e.atoms(Symbol, Dummy))
    if len(syms):
        # Find values of constants for which solutions are equal
        redn = linsolve(e.all_coeffs(), syms)
        if len(redn):
            # Return the general solution over a particular solution
            if len(syms1) > len(syms2):
                return sol2
            # If both have constants, return the lesser complex solution
            elif len(syms1) == len(syms2):
                return sol1 if count_ops(syms1) >= count_ops(syms2) else sol2
            else:
                return sol1

