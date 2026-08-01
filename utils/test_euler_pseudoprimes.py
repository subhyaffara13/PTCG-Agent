
def test_euler_pseudoprimes():
    assert is_euler_pseudoprime(13, 1)
    assert is_euler_pseudoprime(15, 1)
    assert is_euler_pseudoprime(17, 6)
    assert is_euler_pseudoprime(101, 7)
    assert is_euler_pseudoprime(1009, 10)
    assert is_euler_pseudoprime(11287, 41)

    raises(ValueError, lambda: is_euler_pseudoprime(0, 4))
    raises(ValueError, lambda: is_euler_pseudoprime(3, 0))
    raises(ValueError, lambda: is_euler_pseudoprime(15, 6))

    # A006970
    euler_prp = [341, 561, 1105, 1729, 1905, 2047, 2465, 3277,
                 4033, 4681, 5461, 6601, 8321, 8481, 10261, 10585]
    for p in euler_prp:
        assert is_euler_pseudoprime(p, 2)

    # A048950
    euler_prp = [121, 703, 1729, 1891, 2821, 3281, 7381, 8401, 8911, 10585,
                 12403, 15457, 15841, 16531, 18721, 19345, 23521, 24661, 28009]
    for p in euler_prp:
        assert is_euler_pseudoprime(p, 3)

    # A033181
    absolute_euler_prp = [1729, 2465, 15841, 41041, 46657, 75361,
                          162401, 172081, 399001, 449065, 488881]
    for p in absolute_euler_prp:
        for a in range(2, p):
            if gcd(a, p) != 1:
                continue
            assert is_euler_pseudoprime(p, a)

