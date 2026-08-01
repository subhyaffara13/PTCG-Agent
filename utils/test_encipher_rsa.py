
def test_encipher_rsa():
    puk = rsa_public_key(2, 3, 1)
    assert encipher_rsa(2, puk) == 2
    puk = rsa_public_key(5, 3, 3)
    assert encipher_rsa(2, puk) == 8

    with warns(NonInvertibleCipherWarning):
        puk = rsa_public_key(2, 2, 1)
        assert encipher_rsa(2, puk) == 2

