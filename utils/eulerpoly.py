
def eulerpoly(ctx, n, z):
    n = int(n)
    if n < 0:
        raise ValueError("Euler polynomials only defined for n >= 0")
    if n <= 2:
        if n == 0: return z ** 0
        if n == 1: return z - 0.5
        if n == 2: return z*(z-1)
    if ctx.isinf(z):
        return z**n
    if ctx.isnan(z):
        return z
    m = n+1
    if z == 0:
        return -2*(ctx.ldexp(1,m)-1)*ctx.bernoulli(m)/m * z**0
    if z == 1:
        return 2*(ctx.ldexp(1,m)-1)*ctx.bernoulli(m)/m * z**0
    if z == 0.5:
        if n % 2:
            return ctx.zero
        # Use exact code for Euler numbers
        if n < 100 or n*ctx.mag(0.46839865*n) < ctx.prec*0.25:
            return ctx.ldexp(ctx._eulernum(n), -n)
    # http://functions.wolfram.com/Polynomials/EulerE2/06/01/02/01/0002/
    def terms():
        t = ctx.one
        k = 0
        w = ctx.ldexp(1,n+2)
        while 1:
            v = n-k+1
            if not (v > 2 and v & 1):
                yield (2-w)*ctx.bernoulli(v)*t
            k += 1
            if k > n:
                break
            t = t*z*(n-k+2)/k
            w *= 0.5
    return ctx.sum_accurately(terms) / m

