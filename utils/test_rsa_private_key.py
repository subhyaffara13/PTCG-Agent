
def test_rsa_private_key():
    assert rsa_private_key(2, 3, 1) == (6, 1)
    assert rsa_private_key(5, 3, 3) == (15, 3)
    assert rsa_private_key(23,29,5) == (667,493)

    with warns(NonInvertibleCipherWarning):
        assert rsa_private_key(2, 2, 1) == (4, 1)
        assert rsa_private_key(8, 8, 8) is False

