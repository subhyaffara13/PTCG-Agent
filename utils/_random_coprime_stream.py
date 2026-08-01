
def _random_coprime_stream(n, seed=None):
    randrange = _randrange(seed)
    while True:
        y = randrange(n)
        if gcd(y, n) == 1:
            yield y

