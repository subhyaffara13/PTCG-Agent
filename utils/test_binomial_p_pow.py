
def test_binomial_p_pow():
    n, binomials, binomial = 1000, [1], 1
    for i in range(1, n + 1):
        binomial *= n - i + 1
        binomial //= i
        binomials.append(binomial)

    # Test powers of two, which the algorithm treats slightly differently
    trials_2 = 100
    for _ in range(trials_2):
        m, power = randint(0, n), randint(1, 20)
        assert _binomial_mod_prime_power(n, m, 2, power) == binomials[m] % 2**power

    # Test against other prime powers
    primes = list(sieve.primerange(2*n))
    trials = 1000
    for _ in range(trials):
        m, prime, power = randint(0, n), choice(primes), randint(1, 10)
        assert _binomial_mod_prime_power(n, m, prime, power) == binomials[m] % prime**power

