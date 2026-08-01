
def test_rsa_multiprime_exhanstive():
    primes = [3, 5, 7, 11]
    e = 7
    args = primes + [e]
    puk = rsa_public_key(*args, totient='Carmichael')
    prk = rsa_private_key(*args, totient='Carmichael')
    n = puk[0]

    for msg in range(n):
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

