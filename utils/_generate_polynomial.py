
def _generate_polynomial(N, M, factor_base, idx_1000, idx_5000, randint):
    """ Generate sieve polynomials indefinitely.
    Information such as `soln1` in the `factor_base` associated with
    the polynomial is modified in place.

    Parameters
    ==========

    N : Number to be factored
    M : sieve interval
    factor_base : factor_base primes
    idx_1000 : index of prime number in the factor_base near 1000
    idx_5000 : index of prime number in the factor_base near to 5000
    randint : A callable that takes two integers (a, b) and returns a random integer
              n such that a <= n <= b, similar to `random.randint`.
    """
    approx_val = log(2*N)/2 - log(M)
    start = idx_1000 or 0
    end = idx_5000 or (len(factor_base) - 1)
    while True:
        # Choose `a` that is close to `sqrt(2*N) / M`
        best_a, best_q, best_ratio = None, None, None
        for _ in range(50):
            a = 1
            q = []
            while log(a) < approx_val:
                rand_p = 0
                while(rand_p == 0 or rand_p in q):
                    rand_p = randint(start, end)
                p = factor_base[rand_p].prime
                a *= p
                q.append(rand_p)
            ratio = exp(log(a) - approx_val)
            if best_ratio is None or abs(ratio - 1) < abs(best_ratio - 1):
                best_q = q
                best_a = a
                best_ratio = ratio

        # Set `b` using the Chinese remainder theorem
        a = best_a
        q = best_q
        B = []
        for val in q:
            q_l = factor_base[val].prime
            gamma = factor_base[val].tmem_p * invert(a // q_l, q_l) % q_l
            if 2*gamma > q_l:
                gamma = q_l - gamma
            B.append(a//q_l*gamma)
        b = sum(B)
        g = SievePolynomial(a, b, N)
        for fb in factor_base:
            if a % fb.prime == 0:
                fb.soln1 = None
                continue
            a_inv = invert(a, fb.prime)
            fb.b_ainv = [2*b_elem*a_inv % fb.prime for b_elem in B]
            fb.soln1 = (a_inv*(fb.tmem_p - b)) % fb.prime
            fb.soln2 = (a_inv*(-fb.tmem_p - b)) % fb.prime
        yield g

        # Update `b` with Gray code
        for i in range(1, 2**(len(B)-1)):
            v = bit_scan1(i)
            neg_pow = 2*((i >> (v + 1)) % 2) - 1
            b = g.b + 2*neg_pow*B[v]
            a = g.a
            g = SievePolynomial(a, b, N)
            for fb in factor_base:
                if fb.soln1 is None:
                    continue
                fb.soln1 = (fb.soln1 - neg_pow*fb.b_ainv[v]) % fb.prime
                fb.soln2 = (fb.soln2 - neg_pow*fb.b_ainv[v]) % fb.prime
            yield g

