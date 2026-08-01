
def fold_infinite(ctx, f, intervals):
    if len(intervals) < 2:
        return f
    dim1 = intervals[-2][0]
    dim2 = intervals[-1][0]
    # Assume intervals are [0,inf] x [0,inf] x ...
    def g(*args):
        args = list(args)
        #args.insert(dim2, None)
        n = int(args[dim1])
        s = ctx.zero
        #y = ctx.mpf(n)
        args[dim2] = ctx.mpf(n) #y
        for x in xrange(n+1):
            args[dim1] = ctx.mpf(x)
            s += f(*args)
        args[dim1] = ctx.mpf(n) #ctx.mpf(n)
        for y in xrange(n):
            args[dim2] = ctx.mpf(y)
            s += f(*args)
        return s
    #print "Folded infinite from", len(intervals), "to", (len(intervals)-1)
    return fold_infinite(ctx, g, intervals[:-1])

