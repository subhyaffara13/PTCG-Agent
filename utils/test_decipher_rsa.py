
def test_decipher_rsa():
    prk = rsa_private_key(2, 3, 1)
    assert decipher_rsa(2, prk) == 2
    prk = rsa_private_key(5, 3, 3)
    assert decipher_rsa(8, prk) == 2

    with warns(NonInvertibleCipherWarning):
        prk = rsa_private_key(2, 2, 1)
        assert decipher_rsa(2, prk) == 2

