
def test_elgamal_private_key():
    a, b, _ = elgamal_private_key(digit=100)
    assert isprime(a)
    assert is_primitive_root(b, a)
    assert len(bin(a)) >= 102

