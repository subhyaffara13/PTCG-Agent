
def kronecker_mat_add(expr):
    args = sift(expr.args, _kronecker_dims_key)
    nonkrons = args.pop((0,), None)
    if not args:
        return expr

    krons = [reduce(lambda x, y: x._kronecker_add(y), group)
             for group in args.values()]

    if not nonkrons:
        return MatAdd(*krons)
    else:
        return MatAdd(*krons) + nonkrons

