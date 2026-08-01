
def _dummy_with_inherited_properties_concrete(limits):
    """
    Return a Dummy symbol that inherits as many assumptions as possible
    from the provided symbol and limits.

    If the symbol already has all True assumption shared by the limits
    then return None.
    """
    x, a, b = limits
    l = [a, b]

    assumptions_to_consider = ['extended_nonnegative', 'nonnegative',
                               'extended_nonpositive', 'nonpositive',
                               'extended_positive', 'positive',
                               'extended_negative', 'negative',
                               'integer', 'rational', 'finite',
                               'zero', 'real', 'extended_real']

    assumptions_to_keep = {}
    assumptions_to_add = {}
    for assum in assumptions_to_consider:
        assum_true = x._assumptions.get(assum, None)
        if assum_true:
            assumptions_to_keep[assum] = True
        elif all(getattr(i, 'is_' + assum) for i in l):
            assumptions_to_add[assum] = True
    if assumptions_to_add:
        assumptions_to_keep.update(assumptions_to_add)
        return Dummy('d', **assumptions_to_keep)

