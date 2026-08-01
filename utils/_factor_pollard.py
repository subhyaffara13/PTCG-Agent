
def _factor_pollard(n):
    # Return a factor of n using Pollard's rho algorithm.
    # Efficient when n is odd and composite.
    for b in range(1, n):
        x = y = 2
        d = 1
        while d == 1:
            x = (x * x + b) % n
            y = (y * y + b) % n
            y = (y * y + b) % n
            d = gcd(x - y, n)
        if d != n:
            return d
    raise ValueError('prime or under 5')  # pragma: no cover

