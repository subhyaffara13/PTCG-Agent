
def _is_indefinite(M):
    if M.is_hermitian:
        eigen = M.eigenvals()
        args1        = [x.is_positive for x in eigen.keys()]
        any_positive = fuzzy_or(args1)
        args2        = [x.is_negative for x in eigen.keys()]
        any_negative = fuzzy_or(args2)

        return fuzzy_and([any_positive, any_negative])

    elif M.is_square:
        return (M + M.H).is_indefinite

    return False

