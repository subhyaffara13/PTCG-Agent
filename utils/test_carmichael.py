
def test_carmichael():
    with warns_deprecated_sympy():
        assert carmichael.is_prime(2821) == False

