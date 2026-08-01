
def glaisher_fixed(prec):
    wp = prec + 30
    # Number of direct terms to sum before applying the Euler-Maclaurin
    # formula to the tail. TODO: choose more intelligently
    N = int(0.33*prec + 5)
    ONE = MPZ_ONE << wp
    # Euler-Maclaurin, step 1: sum log(k)/k**2 for k from 2 to N-1
    s = MPZ_ZERO
    for k in range(2, N):
        #print k, N
        s += log_int_fixed(k, wp) // k**2
    logN = log_int_fixed(N, wp)
    #logN = to_fixed(mpf_log(from_int(N), wp+20), wp)
    # E-M step 2: integral of log(x)/x**2 from N to inf
    s += (ONE + logN) // N
    # E-M step 3: endpoint correction term f(N)/2
    s += logN // (N**2 * 2)
    # E-M step 4: the series of derivatives
    pN = N**3
    a = 1
    b = -2
    j = 3
    fac = from_int(2)
    k = 1
    while 1:
        # D(2*k-1) * B(2*k) / fac(2*k) [D(n) = nth derivative]
        D = ((a << wp) + b*logN) // pN
        D = from_man_exp(D, -wp)
        B = mpf_bernoulli(2*k, wp)
        term = mpf_mul(B, D, wp)
        term = mpf_div(term, fac, wp)
        term = to_fixed(term, wp)
        if abs(term) < 100:
            break
        #if not k % 10:
        #    print k, math.log(int(abs(term)), 10)
        s -= term
        # Advance derivative twice
        a, b, pN, j = b-a*j, -j*b, pN*N, j+1
        a, b, pN, j = b-a*j, -j*b, pN*N, j+1
        k += 1
        fac = mpf_mul_int(fac, (2*k)*(2*k-1), wp)
    # A = exp((6*s/pi**2 + log(2*pi) + euler)/12)
    pi = pi_fixed(wp)
    s *= 6
    s = (s << wp) // (pi**2 >> wp)
    s += euler_fixed(wp)
    s += to_fixed(mpf_log(from_man_exp(2*pi, -wp), wp), wp)
    s //= 12
    A = mpf_exp(from_man_exp(s, -wp), wp)
    return to_fixed(A, prec)

