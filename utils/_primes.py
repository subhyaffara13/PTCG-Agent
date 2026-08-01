
def _primes(n):
    # Defined to facilitate comparison between translation and source
    # In Matlab, primes(10.5) -> first four primes, primes(11.5) -> first five
    return primes_from_2_to(math.ceil(n))

