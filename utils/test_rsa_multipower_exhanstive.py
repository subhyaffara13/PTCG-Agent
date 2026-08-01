
def test_rsa_multipower_exhanstive():
    primes = [5, 5, 7]
    e = 7
    args = primes + [e]
    puk = rsa_public_key(*args, multipower=True)
    prk = rsa_private_key(*args, multipower=True)
    n = puk[0]

    for msg in range(n):
        if gcd(msg, n) != 1:
            continue

        encrypted = encipher_rsa(msg, puk)
        decrypted = decipher_rsa(encrypted, prk)
        try:
            assert decrypted == msg
        except AssertionError:
            raise AssertionError(
                "The RSA is not correctly decrypted " \
                "(Original : {}, Encrypted : {}, Decrypted : {})" \
                .format(msg, encrypted, decrypted)
                )

