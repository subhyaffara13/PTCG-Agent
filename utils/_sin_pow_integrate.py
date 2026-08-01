
def _sin_pow_integrate(n, x):
    if n > 0:
        if n == 1:
            #Recursion break
            return -cos(x)

        # n > 0
        #  /                                                 /
        # |                                                 |
        # |    n           -1               n-1     n - 1   |     n-2
        # | sin (x) dx =  ______ cos (x) sin (x) + _______  |  sin (x) dx
        # |                                                 |
        # |                 n                         n     |
        #/                                                 /
        #
        #

        return (Rational(-1, n) * cos(x) * sin(x)**(n - 1) +
                Rational(n - 1, n) * _sin_pow_integrate(n - 2, x))

    if n < 0:
        if n == -1:
            ##Make sure this does not come back here again.
            ##Recursion breaks here or at n==0.
            return trigintegrate(1/sin(x), x)

        # n < 0
        #  /                                                 /
        # |                                                 |
        # |    n            1               n+1     n + 2   |     n+2
        # | sin (x) dx = _______ cos (x) sin (x) + _______  |  sin (x) dx
        # |                                                 |
        # |               n + 1                     n + 1   |
        #/                                                 /
        #

        return (Rational(1, n + 1) * cos(x) * sin(x)**(n + 1) +
                Rational(n + 2, n + 1) * _sin_pow_integrate(n + 2, x))

    else:
        #n == 0
        #Recursion break.
        return x

