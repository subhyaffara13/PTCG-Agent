
def test_mod_pow():
    for s, t, u, v in [(4, 13, 497, 445), (4, -3, 497, 365),
            (3.2, 2.1, 1.9, 0.1031015682350942), (S(3)/2, 5, S(5)/6, S(3)/32)]:
        assert pow(S(s), t, u) == v
        assert pow(S(s), S(t), u) == v
        assert pow(S(s), t, S(u)) == v
        assert pow(S(s), S(t), S(u)) == v
    assert pow(S(2), S(10000000000), S(3)) == 1
    assert pow(x, y, z) == x**y%z
    raises(TypeError, lambda: pow(S(4), "13", 497))
    raises(TypeError, lambda: pow(S(4), 13, "497"))

