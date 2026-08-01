
def test_lucas_sequence():
    def lucas_u(P, Q, length):
        array = [0] * length
        array[1] = 1
        for k in range(2, length):
            array[k] = P * array[k - 1] - Q * array[k - 2]
        return array

    def lucas_v(P, Q, length):
        array = [0] * length
        array[0] = 2
        array[1] = P
        for k in range(2, length):
            array[k] = P * array[k - 1] - Q * array[k - 2]
        return array

    length = 20
    for P in range(-10, 10):
        for Q in range(-10, 10):
            D = P**2 - 4*Q
            if D == 0:
                continue
            us = lucas_u(P, Q, length)
            vs = lucas_v(P, Q, length)
            for n in range(3, 100, 2):
                for k in range(length):
                    U, V, Qk = _lucas_sequence(n, P, Q, k)
                    assert U == us[k] % n
                    assert V == vs[k] % n
                    assert pow(Q, k, n) == Qk

