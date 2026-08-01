
def siegeltheta(ctx, t, derivative=0):
    d = int(derivative)
    if  (t == ctx.inf or t == ctx.ninf):
        if d < 2:
            if t == ctx.ninf and d == 0:
                return ctx.ninf
            return ctx.inf
        else:
            return ctx.zero
    if d == 0:
        if ctx._im(t):
            # XXX: cancellation occurs
            a = ctx.loggamma(0.25+0.5j*t)
            b = ctx.loggamma(0.25-0.5j*t)
            return -ctx.ln(ctx.pi)/2*t - 0.5j*(a-b)
        else:
            if ctx.isinf(t):
                return t
            return ctx._im(ctx.loggamma(0.25+0.5j*t)) - ctx.ln(ctx.pi)/2*t
    if d > 0:
        a = (-0.5j)**(d-1)*ctx.polygamma(d-1, 0.25-0.5j*t)
        b = (0.5j)**(d-1)*ctx.polygamma(d-1, 0.25+0.5j*t)
        if ctx._im(t):
            if d == 1:
                return -0.5*ctx.log(ctx.pi)+0.25*(a+b)
            else:
                return 0.25*(a+b)
        else:
            if d == 1:
                return ctx._re(-0.5*ctx.log(ctx.pi)+0.25*(a+b))
            else:
                return ctx._re(0.25*(a+b))

