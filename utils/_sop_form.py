
def _sop_form(variables, minterms, dontcares):
    new = _simplified_pairs(minterms + dontcares)
    essential = _rem_redundancy(new, minterms)
    return Or(*[_convert_to_varsSOP(x, variables) for x in essential])

