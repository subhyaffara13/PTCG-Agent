
def ifib(n, _cache={}):
    """Computes the nth Fibonacci number as an integer, for
    integer n."""
    if n < 0:
        return (-1)**(-n+1) * ifib(-n)
    if n in _cache:
        return _cache[n]
    m = n
    # Use Dijkstra's logarithmic algorithm
    # The following implementation is basically equivalent to
    # http://en.literateprograms.org/Fibonacci_numbers_(Scheme)
    a, b, p, q = MPZ_ONE, MPZ_ZERO, MPZ_ZERO, MPZ_ONE
    while n:
        if n & 1:
            aq = a*q
            a, b = b*q+aq+a*p, b*p+aq
            n -= 1
        else:
            qq = q*q
            p, q = p*p+qq, qq+2*p*q
            n >>= 1
    if m < 250:
        _cache[m] = b
    return b

