
def cycle_length(f, x0, nmax=None, values=False):
    """For a given iterated sequence, return a generator that gives
    the length of the iterated cycle (lambda) and the length of terms
    before the cycle begins (mu); if ``values`` is True then the
    terms of the sequence will be returned instead. The sequence is
    started with value ``x0``.

    Note: more than the first lambda + mu terms may be returned and this
    is the cost of cycle detection with Brent's method; there are, however,
    generally less terms calculated than would have been calculated if the
    proper ending point were determined, e.g. by using Floyd's method.

    >>> from sympy.ntheory.generate import cycle_length

    This will yield successive values of i <-- func(i):

        >>> def gen(func, i):
        ...     while 1:
        ...         yield i
        ...         i = func(i)
        ...

    A function is defined:

        >>> func = lambda i: (i**2 + 1) % 51

    and given a seed of 4 and the mu and lambda terms calculated:

        >>> next(cycle_length(func, 4))
        (6, 3)

    We can see what is meant by looking at the output:

        >>> iter = cycle_length(func, 4, values=True)
        >>> list(iter)
        [4, 17, 35, 2, 5, 26, 14, 44, 50, 2, 5, 26, 14]

    There are 6 repeating values after the first 3.

    If a sequence is suspected of being longer than you might wish, ``nmax``
    can be used to exit early (and mu will be returned as None):

        >>> next(cycle_length(func, 4, nmax = 4))
        (4, None)
        >>> list(cycle_length(func, 4, nmax = 4, values=True))
        [4, 17, 35, 2]

    Code modified from:
        https://en.wikipedia.org/wiki/Cycle_detection.
    """

    nmax = int(nmax or 0)

    # main phase: search successive powers of two
    power = lam = 1
    tortoise, hare = x0, f(x0)  # f(x0) is the element/node next to x0.
    i = 1
    if values:
        yield tortoise
    while tortoise != hare and (not nmax or i < nmax):
        i += 1
        if power == lam:   # time to start a new power of two?
            tortoise = hare
            power *= 2
            lam = 0
        if values:
            yield hare
        hare = f(hare)
        lam += 1
    if nmax and i == nmax:
        if values:
            return
        else:
            yield nmax, None
            return
    if not values:
        # Find the position of the first repetition of length lambda
        mu = 0
        tortoise = hare = x0
        for i in range(lam):
            hare = f(hare)
        while tortoise != hare:
            tortoise = f(tortoise)
            hare = f(hare)
            mu += 1
        yield lam, mu

