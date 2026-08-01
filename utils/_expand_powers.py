
def _expand_powers(factors):
    """
    Helper function for normal_ordered_form and normal_order: Expand a
    power expression to a multiplication expression so that that the
    expression can be handled by the normal ordering functions.
    """

    new_factors = []
    for factor in factors.args:
        if (isinstance(factor, Pow)
                and isinstance(factor.args[1], Integer)
                and factor.args[1] > 0):
            for n in range(factor.args[1]):
                new_factors.append(factor.args[0])
        else:
            new_factors.append(factor)

    return new_factors

