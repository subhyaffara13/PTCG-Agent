
def linsolve_dict(eq, syms):
    """
    Get the output of linsolve as a dict
    """
    # Convert tuple type return value of linsolve
    # to a dictionary for ease of use
    sol = linsolve(eq, syms)
    if not sol:
        return {}
    return dict(zip(syms, list(sol)[0]))

