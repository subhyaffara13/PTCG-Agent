
def mcmahon(ctx,kind,prime,v,m):
    """
    Computes an estimate for the location of the Bessel function zero
    j_{v,m}, y_{v,m}, j'_{v,m} or y'_{v,m} using McMahon's asymptotic
    expansion (Abramowitz & Stegun 9.5.12-13, DLMF 20.21(vi)).

    Returns (r,err) where r is the estimated location of the root
    and err is a positive number estimating the error of the
    asymptotic expansion.
    """
    u = 4*v**2
    if kind == 1 and not prime: b = (4*m+2*v-1)*ctx.pi/4
    if kind == 2 and not prime: b = (4*m+2*v-3)*ctx.pi/4
    if kind == 1 and prime: b = (4*m+2*v-3)*ctx.pi/4
    if kind == 2 and prime: b = (4*m+2*v-1)*ctx.pi/4
    if not prime:
        s1 = b
        s2 = -(u-1)/(8*b)
        s3 = -4*(u-1)*(7*u-31)/(3*(8*b)**3)
        s4 = -32*(u-1)*(83*u**2-982*u+3779)/(15*(8*b)**5)
        s5 = -64*(u-1)*(6949*u**3-153855*u**2+1585743*u-6277237)/(105*(8*b)**7)
    if prime:
        s1 = b
        s2 = -(u+3)/(8*b)
        s3 = -4*(7*u**2+82*u-9)/(3*(8*b)**3)
        s4 = -32*(83*u**3+2075*u**2-3039*u+3537)/(15*(8*b)**5)
        s5 = -64*(6949*u**4+296492*u**3-1248002*u**2+7414380*u-5853627)/(105*(8*b)**7)
    terms = [s1,s2,s3,s4,s5]
    s = s1
    err = 0.0
    for i in range(1,len(terms)):
        if abs(terms[i]) < abs(terms[i-1]):
            s += terms[i]
        else:
            err = abs(terms[i])
    if i == len(terms)-1:
        err = abs(terms[-1])
    return s, err

