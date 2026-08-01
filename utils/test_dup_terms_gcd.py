
def test_dup_terms_gcd():
    assert dup_terms_gcd([], ZZ) == (0, [])
    assert dup_terms_gcd([1, 0, 1], ZZ) == (0, [1, 0, 1])
    assert dup_terms_gcd([1, 0, 1, 0], ZZ) == (1, [1, 0, 1])

