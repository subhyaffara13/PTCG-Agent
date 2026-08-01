
def _convert_to_varsPOS(maxterm, variables):
    """
    Converts a term in the expansion of a function from binary to its
    variable form (for POS).
    """
    temp = [variables[n] if val == 0 else Not(variables[n])
            for n, val in enumerate(maxterm) if val != 3]
    return Or(*temp)

