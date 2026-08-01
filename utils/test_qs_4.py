
def test_qs_4():
    N = 10007**2 * 10009 * 10037**3 * 10039
    for factor in qs(N, 1000, 2000):
        assert N % factor == 0
        N //= factor

