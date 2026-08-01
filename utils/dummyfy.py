
def dummyfy(args, exprs):
    # TODO Is this a good idea?
    d_args = Matrix([s.as_dummy() for s in args])
    reps = dict(zip(args, d_args))
    d_exprs = Matrix([_sympify(expr).subs(reps) for expr in exprs])
    return d_args, d_exprs

