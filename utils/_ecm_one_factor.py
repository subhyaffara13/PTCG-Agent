
def _ecm_one_factor(n, B1=10000, B2=100000, max_curve=200, seed=None):
    """Returns one factor of n using
    Lenstra's 2 Stage Elliptic curve Factorization
    with Suyama's Parameterization. Here Montgomery
    arithmetic is used for fast computation of addition
    and doubling of points in elliptic curve.

    Explanation
    ===========

    This ECM method considers elliptic curves in Montgomery
    form (E : b*y**2*z = x**3 + a*x**2*z + x*z**2) and involves
    elliptic curve operations (mod N), where the elements in
    Z are reduced (mod N). Since N is not a prime, E over FF(N)
    is not really an elliptic curve but we can still do point additions
    and doubling as if FF(N) was a field.

    Stage 1 : The basic algorithm involves taking a random point (P) on an
    elliptic curve in FF(N). The compute k*P using Montgomery ladder algorithm.
    Let q be an unknown factor of N. Then the order of the curve E, |E(FF(q))|,
    might be a smooth number that divides k. Then we have k = l * |E(FF(q))|
    for some l. For any point belonging to the curve E, |E(FF(q))|*P = O,
    hence k*P = l*|E(FF(q))|*P. Thus kP.z_cord = 0 (mod q), and the unknownn
    factor of N (q) can be recovered by taking gcd(kP.z_cord, N).

    Stage 2 : This is a continuation of Stage 1 if k*P != O. The idea utilize
    the fact that even if kP != 0, the value of k might miss just one large
    prime divisor of |E(FF(q))|. In this case we only need to compute the
    scalar multiplication by p to get p*k*P = O. Here a second bound B2
    restrict the size of possible values of p.

    Parameters
    ==========

    n : Number to be Factored. Assume that it is a composite number.
    B1 : Stage 1 Bound. Must be an even number.
    B2 : Stage 2 Bound. Must be an even number.
    max_curve : Maximum number of curves generated

    Returns
    =======

    integer | None : a non-trivial divisor of ``n``. ``None`` if not found

    References
    ==========

    .. [1] Carl Pomerance, Richard Crandall, Prime Numbers: A Computational Perspective,
           2nd Edition (2005), page 344, ISBN:978-0387252827
    """
    randint = _randint(seed)

    # When calculating T, if (B1 - 2*D) is negative, it cannot be calculated.
    D = min(sqrt(B2), B1 // 2 - 1)
    sieve.extend(D)
    beta = [0] * D
    S = [0] * D
    k = 1
    for p in primerange(2, B1 + 1):
        k *= pow(p, int(log(B1, p)))

    # Pre-calculate the prime numbers to be used in stage 2.
    # Using the fact that the x-coordinates of point P and its
    # inverse -P coincide, the number of primes to be checked
    # in stage 2 can be reduced.
    deltas_list = []
    for r in range(B1 + 2*D, B2 + 2*D, 4*D):
        # d in deltas iff r+(2d+1) and/or r-(2d+1) is prime
        deltas = {abs(q - r) >> 1 for q in primerange(r - 2*D, r + 2*D)}
        deltas_list.append(list(deltas))

    for _ in range(max_curve):
        #Suyama's Parametrization
        sigma = randint(6, n - 1)
        u = (sigma**2 - 5) % n
        v = (4*sigma) % n
        u_3 = pow(u, 3, n)

        try:
            # We use the elliptic curve y**2 = x**3 + a*x**2 + x
            # where a = pow(v - u, 3, n)*(3*u + v)*invert(4*u_3*v, n) - 2
            # However, we do not declare a because it is more convenient
            # to use a24 = (a + 2)*invert(4, n) in the calculation.
            a24 = pow(v - u, 3, n)*(3*u + v)*invert(16*u_3*v, n) % n
        except ZeroDivisionError:
            #If the invert(16*u_3*v, n) doesn't exist (i.e., g != 1)
            g = gcd(2*u_3*v, n)
            #If g = n, try another curve
            if g == n:
                continue
            return g

        Q = Point(u_3, pow(v, 3, n), a24, n)
        Q = Q.mont_ladder(k)
        g = gcd(Q.z_cord, n)

        #Stage 1 factor
        if g != 1 and g != n:
            return g
        #Stage 1 failure. Q.z = 0, Try another curve
        elif g == n:
            continue

        #Stage 2 - Improved Standard Continuation
        S[0] = Q
        Q2 = Q.double()
        S[1] = Q2.add(Q, Q)
        beta[0] = (S[0].x_cord*S[0].z_cord) % n
        beta[1] = (S[1].x_cord*S[1].z_cord) % n
        for d in range(2, D):
            S[d] = S[d - 1].add(Q2, S[d - 2])
            beta[d] = (S[d].x_cord*S[d].z_cord) % n
        # i.e., S[i] = Q.mont_ladder(2*i + 1)

        g = 1
        W = Q.mont_ladder(4*D)
        T = Q.mont_ladder(B1 - 2*D)
        R = Q.mont_ladder(B1 + 2*D)
        for deltas in deltas_list:
            # R = Q.mont_ladder(r) where r in range(B1 + 2*D, B2 + 2*D, 4*D)
            alpha = (R.x_cord*R.z_cord) % n
            for delta in deltas:
                # We want to calculate
                # f = R.x_cord * S[delta].z_cord - S[delta].x_cord * R.z_cord
                f = (R.x_cord - S[delta].x_cord)*\
                    (R.z_cord + S[delta].z_cord) - alpha + beta[delta]
                g = (g*f) % n
            T, R = R, R.add(W, T)
        g = gcd(n, g)

        #Stage 2 Factor found
        if g != 1 and g != n:
            return g

