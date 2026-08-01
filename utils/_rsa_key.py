
def _rsa_key(*args, public=True, private=True, totient='Euler', index=None, multipower=None):
    r"""A private subroutine to generate RSA key

    Parameters
    ==========

    public, private : bool, optional
        Flag to generate either a public key, a private key.

    totient : 'Euler' or 'Carmichael'
        Different notation used for totient.

    multipower : bool, optional
        Flag to bypass warning for multipower RSA.
    """

    if len(args) < 2:
        return False

    if totient not in ('Euler', 'Carmichael'):
        raise ValueError(
            "The argument totient={} should either be " \
            "'Euler', 'Carmichalel'." \
            .format(totient))

    if totient == 'Euler':
        _totient = _euler
    else:
        _totient = _carmichael

    if index is not None:
        index = as_int(index)
        if totient != 'Carmichael':
            raise ValueError(
                "Setting the 'index' keyword argument requires totient"
                "notation to be specified as 'Carmichael'.")

    primes, e = args[:-1], args[-1]

    if not all(isprime(p) for p in primes):
        new_primes = []
        for i in primes:
            new_primes.extend(factorint(i, multiple=True))
        primes = new_primes

    n = reduce(lambda i, j: i*j, primes)

    tally = multiset(primes)
    if all(v == 1 for v in tally.values()):
        phi = int(_totient(tally))

    else:
        if not multipower:
            NonInvertibleCipherWarning(
                'Non-distinctive primes found in the factors {}. '
                'The cipher may not be decryptable for some numbers '
                'in the complete residue system Z[{}], but the cipher '
                'can still be valid if you restrict the domain to be '
                'the reduced residue system Z*[{}]. You can pass '
                'the flag multipower=True if you want to suppress this '
                'warning.'
                .format(primes, n, n)
                # stacklevel=4 because most users will call a function that
                # calls this function
                ).warn(stacklevel=4)
        phi = int(_totient(tally))

    if gcd(e, phi) == 1:
        if public and not private:
            if isinstance(index, int):
                e = e % phi
                e += index * phi
            return n, e

        if private and not public:
            d = invert(e, phi)
            if isinstance(index, int):
                d += index * phi
            return n, d

    return False

