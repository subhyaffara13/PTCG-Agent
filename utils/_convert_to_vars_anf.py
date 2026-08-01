
def _convert_to_varsANF(term, variables):
    """
    Converts a term in the expansion of a function from binary to its
    variable form (for ANF).

    Parameters
    ==========

    term : list of 1's and 0's (complementation pattern)
    variables : list of variables

    """
    temp = [variables[n] for n, t in enumerate(term) if t == 1]

    if not temp:
        return true

    return And(*temp)

