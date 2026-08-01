
def test_private_perfect_power():
    assert _perfect_power(0) is False
    assert _perfect_power(1) is False
    assert _perfect_power(2) is False
    assert _perfect_power(3) is False
    for x in [2, 3, 5, 6, 7, 12, 15, 105, 100003]:
        for y in range(2, 100):
            assert _perfect_power(x**y) == (x, y)
            if x & 1:
                assert _perfect_power(x**y, next_p=3) == (x, y)
            if x == 100003:
                assert _perfect_power(x**y, next_p=100003) == (x, y)
            assert _perfect_power(101*x**y) == False
            # Catalan's conjecture
            if x**y not in [8, 9]:
                assert _perfect_power(x**y + 1) == False
                assert _perfect_power(x**y - 1) == False
    for x in range(1, 10):
        for y in range(1, 10):
            g = gcd(x, y)
            if g == 1:
                assert _perfect_power(5**x * 101**y) == False
            else:
                assert _perfect_power(5**x * 101**y) == (5**(x//g) * 101**(y//g), g)

