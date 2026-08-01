
def _dup_cyclotomic_decompose(n, K):
    from sympy.ntheory import factorint

    H = [[K.one, -K.one]]

    for p, k in factorint(n).items():
        Q = [ dup_quo(dup_inflate(h, p, K), h, K) for h in H ]
        H.extend(Q)

        for i in range(1, k):
            Q = [ dup_inflate(q, p, K) for q in Q ]
            H.extend(Q)

    return H

