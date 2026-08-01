
def test_perfect_power():
    raises(ValueError, lambda: perfect_power(0.1))
    assert perfect_power(0) is False
    assert perfect_power(1) is False
    assert perfect_power(2) is False
    assert perfect_power(3) is False
    assert perfect_power(4) == (2, 2)
    assert perfect_power(14) is False
    assert perfect_power(25) == (5, 2)
    assert perfect_power(22) is False
    assert perfect_power(22, [2]) is False
    assert perfect_power(137**(3*5*13)) == (137, 3*5*13)
    assert perfect_power(137**(3*5*13) + 1) is False
    assert perfect_power(137**(3*5*13) - 1) is False
    assert perfect_power(103005006004**7) == (103005006004, 7)
    assert perfect_power(103005006004**7 + 1) is False
    assert perfect_power(103005006004**7 - 1) is False
    assert perfect_power(103005006004**12) == (103005006004, 12)
    assert perfect_power(103005006004**12 + 1) is False
    assert perfect_power(103005006004**12 - 1) is False
    assert perfect_power(2**10007) == (2, 10007)
    assert perfect_power(2**10007 + 1) is False
    assert perfect_power(2**10007 - 1) is False
    assert perfect_power((9**99 + 1)**60) == (9**99 + 1, 60)
    assert perfect_power((9**99 + 1)**60 + 1) is False
    assert perfect_power((9**99 + 1)**60 - 1) is False
    assert perfect_power((10**40000)**2, big=False) == (10**40000, 2)
    assert perfect_power(10**100000) == (10, 100000)
    assert perfect_power(10**100001) == (10, 100001)
    assert perfect_power(13**4, [3, 5]) is False
    assert perfect_power(3**4, [3, 10], factor=0) is False
    assert perfect_power(3**3*5**3) == (15, 3)
    assert perfect_power(2**3*5**5) is False
    assert perfect_power(2*13**4) is False
    assert perfect_power(2**5*3**3) is False
    t = 2**24
    for d in divisors(24):
        m = perfect_power(t*3**d)
        assert m and m[1] == d or d == 1
        m = perfect_power(t*3**d, big=False)
        assert m and m[1] == 2 or d == 1 or d == 3, (d, m)

    # negatives and non-integer rationals
    assert perfect_power(-4) is False
    assert perfect_power(-8) == (-2, 3)
    assert perfect_power(-S(1)/8) == (-S(1)/2, 3)
    assert perfect_power(S(1)/3) == False
    assert perfect_power(-5**15) == (-5, 15)
    assert perfect_power(-5**15, big=False) == (-3125, 3)
    assert perfect_power(-5**15, [15]) == (-5, 15)

    n = -3 ** 60
    assert perfect_power(n) == (-81, 15)
    assert perfect_power(n, big=False) == (-3486784401, 3)
    assert perfect_power(n, [3, 5], big=True) == (-531441, 5)
    assert perfect_power(n, [3, 5], big=False) == (-3486784401, 3)
    assert perfect_power(n, [2]) == False
    assert perfect_power(n, [2, 15]) == (-81, 15)
    assert perfect_power(n, [2, 13]) == False
    assert perfect_power(n, [17]) == False
    assert perfect_power(n, [3]) == (-3486784401, 3)
    assert perfect_power(n + 1) == False

    r = S(2) ** (2 * 5 * 7) / S(3) ** (2 * 7)
    assert perfect_power(r) == (S(32) / 3, 14)
    assert perfect_power(-r) == (-S(1024) / 9, 7)
    assert perfect_power(r, big=False) == (S(34359738368) / 2187, 2)
    assert perfect_power(r, [2, 5]) == (S(34359738368) / 2187, 2)
    assert perfect_power(r, [5, 7]) == (S(1024) / 9, 7)
    assert perfect_power(r, [5, 7], big=False) == (S(1024) / 9, 7)
    assert perfect_power(r, [2, 5, 7], big=False) == (S(34359738368) / 2187, 2)
    assert perfect_power(-r, [5, 7], big=False) == (-S(1024) / 9, 7)

    assert perfect_power(-S(1) / 8) == (-S(1) / 2, 3)

    assert perfect_power((-3)**60) == (3, 60)
    assert perfect_power((-3)**61) == (-3, 61)

    assert perfect_power(S(2 ** 9) / 3 ** 12) == (S(8)/81, 3)
    assert perfect_power(Rational(1, 2)**3) == (S.Half, 3)
    assert perfect_power(Rational(-3, 2)**3) == (-3*S.Half, 3)

