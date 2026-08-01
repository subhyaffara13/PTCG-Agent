
def test_equal_valued():
    x = Symbol('x')

    equal_values = [
        [1, 1.0, S(1), S(1.0), S(1).n(5)],
        [2, 2.0, S(2), S(2.0), S(2).n(5)],
        [-1, -1.0, -S(1), -S(1.0), -S(1).n(5)],
        [0.5, S(0.5), S(1)/2],
        [-0.5, -S(0.5), -S(1)/2],
        [0, 0.0, S(0), S(0.0), S(0).n()],
        [pi], [pi.n()],           # <-- not equal
        [S(1)/10], [0.1, S(0.1)], # <-- not equal
        [S(0.1).n(5)],
        [oo],
        [cos(x/2)], [cos(0.5*x)], # <-- no recursion
    ]

    for m, values_m in enumerate(equal_values):
        for value_i in values_m:

            # All values in same list equal
            for value_j in values_m:
                assert equal_valued(value_i, value_j) is True

            # Not equal to anything in any other list:
            for n, values_n in enumerate(equal_values):
                if n == m:
                    continue
                for value_j in values_n:
                    assert equal_valued(value_i, value_j) is False

