
def standardize_infinite(ctx, f, intervals):
    if not intervals:
        return f
    dim, [a,b] = intervals[-1]
    if a == ctx.ninf:
        if b == ctx.inf:
            def g(*args):
                args = list(args)
                k = args[dim]
                if k:
                    s = f(*args)
                    args[dim] = -k
                    s += f(*args)
                    return s
                else:
                    return f(*args)
        else:
            def g(*args):
                args = list(args)
                args[dim] = b - args[dim]
                return f(*args)
    else:
        def g(*args):
            args = list(args)
            args[dim] += a
            return f(*args)
    #print "Standardized infinity along dimension", dim, a, b
    return standardize_infinite(ctx, g, intervals[:-1])

