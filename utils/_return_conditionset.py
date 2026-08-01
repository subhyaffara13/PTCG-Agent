
def _return_conditionset(eqs, symbols):
    # return conditionset
    eqs = (Eq(lhs, 0) for lhs in eqs)
    condition_set = ConditionSet(
        Tuple(*symbols), And(*eqs), S.Complexes**len(symbols))
    return condition_set

