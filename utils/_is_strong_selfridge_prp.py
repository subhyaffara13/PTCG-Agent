
def _is_strong_selfridge_prp(n):
    for D in range(5, 1_000_000, 2):
        if D & 2: # if D % 4 == 3
            D = -D
        j = jacobi(D, n)
        if j == -1:
            s = bit_scan1(n + 1)
            U, V, Qk = _lucas_sequence(n, 1, (1-D) // 4, (n + 1) >> s)
            if U == 0 or V == 0:
                return True
            for _ in range(s - 1):
                V = (V*V - 2*Qk) % n
                if V == 0:
                    return True
                Qk = pow(Qk, 2, n)
            return False
        if j == 0 and D % n:
            return False
        # When j == -1 is hard to find, suspect a square number
        if D == 13 and is_square(n):
            return False
    raise ValueError("appropriate value for D cannot be found in is_strong_selfridge_prp()")

