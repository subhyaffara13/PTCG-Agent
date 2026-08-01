
def nest_permutation(expr):
    if isinstance(expr, PermuteDims):
        return expr.nest_permutation()
    else:
        return expr

