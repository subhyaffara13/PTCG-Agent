
def test_dh_private_key():
    p, g, _ = dh_private_key(digit = 100)
    assert isprime(p)
    assert is_primitive_root(g, p)
    assert len(bin(p)) >= 102

