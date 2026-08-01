
def _convert_to_varsSOP(minterm, variables):
    """
    Converts a term in the expansion of a function from binary to its
    variable form (for SOP).
    """
    temp = [variables[n] if val == 1 else Not(variables[n])
            for n, val in enumerate(minterm) if val != 3]
    return And(*temp)

