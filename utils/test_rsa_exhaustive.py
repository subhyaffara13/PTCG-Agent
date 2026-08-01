
def test_rsa_exhaustive():
    p, q = 61, 53
    e = 17
    puk = rsa_public_key(p, q, e, totient='Carmichael')
    prk = rsa_private_key(p, q, e, totient='Carmichael')

    for msg in range(puk[0]):
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

