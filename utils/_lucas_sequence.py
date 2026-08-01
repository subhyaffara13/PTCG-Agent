
def _lucas_sequence(n, P, Q, k):
    r"""Return the modular Lucas sequence (U_k, V_k, Q_k).

    Explanation
    ===========

    Given a Lucas sequence defined by P, Q, returns the kth values for
    U and V, along with Q^k, all modulo n. This is intended for use with
    possibly very large values of n and k, where the combinatorial functions
    would be completely unusable.

    .. math ::
        U_k = \begin{cases}
             0 & \text{if } k = 0\\
             1 & \text{if } k = 1\\
             PU_{k-1} - QU_{k-2} & \text{if } k > 1
        \end{cases}\\
        V_k = \begin{cases}
             2 & \text{if } k = 0\\
             P & \text{if } k = 1\\
             PV_{k-1} - QV_{k-2} & \text{if } k > 1
        \end{cases}

    The modular Lucas sequences are used in numerous places in number theory,
    especially in the Lucas compositeness tests and the various n + 1 proofs.

    Parameters
    ==========

    n : int
        n is an odd number greater than or equal to 3
    P : int
    Q : int
        D determined by D = P**2 - 4*Q is non-zero
    k : int
        k is a nonnegative integer

    Returns
    =======

    U, V, Qk : (int, int, int)
        `(U_k \bmod{n}, V_k \bmod{n}, Q^k \bmod{n})`

    Examples
    ========

    >>> from sympy.external.ntheory import _lucas_sequence
    >>> N = 10**2000 + 4561
    >>> sol = U, V, Qk = _lucas_sequence(N, 3, 1, N//2); sol
    (0, 2, 1)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Lucas_sequence

    """
    if k == 0:
        return (0, 2, 1)
    D = P**2 - 4*Q
    U = 1
    V = P
    Qk = Q % n
    if Q == 1:
        # Optimization for extra strong tests.
        for b in bin(k)[3:]:
            U = (U*V) % n
            V = (V*V - 2) % n
            if b == "1":
                U, V = U*P + V, V*P + U*D
                if U & 1:
                    U += n
                if V & 1:
                    V += n
                U, V = U >> 1, V >> 1
    elif P == 1 and Q == -1:
        # Small optimization for 50% of Selfridge parameters.
        for b in bin(k)[3:]:
            U = (U*V) % n
            if Qk == 1:
                V = (V*V - 2) % n
            else:
                V = (V*V + 2) % n
                Qk = 1
            if b == "1":
                # new_U = (U + V) // 2
                # new_V = (5*U + V) // 2 = 2*U + new_U
                U, V  = U + V, U << 1
                if U & 1:
                    U += n
                U >>= 1
                V += U
                Qk = -1
        Qk %= n
    elif P == 1:
        for b in bin(k)[3:]:
            U = (U*V) % n
            V = (V*V - 2*Qk) % n
            Qk *= Qk
            if b == "1":
                # new_U = (U + V) // 2
                # new_V = new_U - 2*Q*U
                U, V  = U + V, (Q*U) << 1
                if U & 1:
                    U += n
                U >>= 1
                V = U - V
                Qk *= Q
            Qk %= n
    else:
        # The general case with any P and Q.
        for b in bin(k)[3:]:
            U = (U*V) % n
            V = (V*V - 2*Qk) % n
            Qk *= Qk
            if b == "1":
                U, V = U*P + V, V*P + U*D
                if U & 1:
                    U += n
                if V & 1:
                    V += n
                U, V = U >> 1, V >> 1
                Qk *= Q
            Qk %= n
    return (U % n, V % n, Qk)

