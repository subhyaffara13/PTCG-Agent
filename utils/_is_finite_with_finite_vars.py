
def _is_finite_with_finite_vars(f, domain=S.Complexes):
    """
    Return True if the given expression is finite. For symbols that
    do not assign a value for `complex` and/or `real`, the domain will
    be used to assign a value; symbols that do not assign a value
    for `finite` will be made finite. All other assumptions are
    left unmodified.
    """
    def assumptions(s):
        A = s.assumptions0
        A.setdefault('finite', A.get('finite', True))
        if domain.is_subset(S.Reals):
            # if this gets set it will make complex=True, too
            A.setdefault('real', True)
        else:
            # don't change 'real' because being complex implies
            # nothing about being real
            A.setdefault('complex', True)
        return A

    reps = {s: Dummy(**assumptions(s)) for s in f.free_symbols}
    return f.xreplace(reps).is_finite

