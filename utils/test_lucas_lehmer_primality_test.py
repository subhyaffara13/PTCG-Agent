
def test_lucas_lehmer_primality_test():
    for p in sieve.primerange(3, 100):
        assert _lucas_lehmer_primality_test(p) == (p in MERSENNE_PRIME_EXPONENTS)

