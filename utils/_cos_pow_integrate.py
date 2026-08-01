
def _cos_pow_integrate(n, x):
    if n > 0:
        if n == 1:
            #Recursion break.
            return sin(x)

        # n > 0
        #  /                                                 /
        # |                                                 |
        # |    n            1               n-1     n - 1   |     n-2
        # | sin (x) dx =  ______ sin (x) cos (x) + _______  |  cos (x) dx
        # |                                                 |
        # |                 n                         n     |
        #/                                                 /
        #

        return (Rational(1, n) * sin(x) * cos(x)**(n - 1) +
                Rational(n - 1, n) * _cos_pow_integrate(n - 2, x))

    if n < 0:
        if n == -1:
            ##Recursion break
            return trigintegrate(1/cos(x), x)

        # n < 0
        #  /                                                 /
        # |                                                 |
        # |    n            -1              n+1     n + 2   |     n+2
        # | cos (x) dx = _______ sin (x) cos (x) + _______  |  cos (x) dx
        # |                                                 |
        # |               n + 1                     n + 1   |
        #/                                                 /
        #

        return (Rational(-1, n + 1) * sin(x) * cos(x)**(n + 1) +
                Rational(n + 2, n + 1) * _cos_pow_integrate(n + 2, x))
    else:
        # n == 0
        #Recursion Break.
        return x

