
def test_gf_csolve():
    assert gf_value([1, 7, 2, 4], 11) == 2204

    assert linear_congruence(4, 3, 5) == [2]
    assert linear_congruence(0, 3, 5) == []
    assert linear_congruence(6, 1, 4) == []
    assert linear_congruence(0, 5, 5) == [0, 1, 2, 3, 4]
    assert linear_congruence(3, 12, 15) == [4, 9, 14]
    assert linear_congruence(6, 0, 18) == [0, 3, 6, 9, 12, 15]
    # _csolve_prime_las_vegas
    assert _csolve_prime_las_vegas([2, 3, 1], 5) == [2, 4]
    assert _csolve_prime_las_vegas([2, 0, 1], 5) == []
    from sympy.ntheory import primerange
    for p in primerange(2, 100):
        # f = x**(p-1) - 1
        f = gf_sub_ground(gf_pow([1, 0], p - 1, p, ZZ), 1, p, ZZ)
        assert _csolve_prime_las_vegas(f, p) == list(range(1, p))
    # with power = 1
    assert csolve_prime([1, 3, 2, 17], 7) == [3]
    assert csolve_prime([1, 3, 1, 5], 5) == [0, 1]
    assert csolve_prime([3, 6, 9, 3], 3) == [0, 1, 2]
    # with power > 1
    assert csolve_prime(
        [1, 1, 223], 3, 4) == [4, 13, 22, 31, 40, 49, 58, 67, 76]
    assert csolve_prime([3, 5, 2, 25], 5, 3) == [16, 50, 99]
    assert csolve_prime([3, 2, 2, 49], 7, 3) == [147, 190, 234]

    assert gf_csolve([1, 1, 7], 189) == [13, 49, 76, 112, 139, 175]
    assert gf_csolve([1, 3, 4, 1, 30], 60) == [10, 30]
    assert gf_csolve([1, 1, 7], 15) == []

