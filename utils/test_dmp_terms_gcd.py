
def test_dmp_terms_gcd():
    assert dmp_terms_gcd([[]], 1, ZZ) == ((0, 0), [[]])

    assert dmp_terms_gcd([1, 0, 1, 0], 0, ZZ) == ((1,), [1, 0, 1])
    assert dmp_terms_gcd([[1], [], [1], []], 1, ZZ) == ((1, 0), [[1], [], [1]])

    assert dmp_terms_gcd(
        [[1, 0], [], [1]], 1, ZZ) == ((0, 0), [[1, 0], [], [1]])
    assert dmp_terms_gcd(
        [[1, 0], [1, 0, 0], [], []], 1, ZZ) == ((2, 1), [[1], [1, 0]])

