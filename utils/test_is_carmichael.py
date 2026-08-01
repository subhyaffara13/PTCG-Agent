
def test_is_carmichael():
    A002997 = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841,
               29341, 41041, 46657, 52633, 62745, 63973, 75361, 101101]
    for n in range(1, 5000):
        assert is_carmichael(n) == (n in A002997)
    for n in A002997:
        assert is_carmichael(n)

