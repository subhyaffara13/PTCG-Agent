
def test_exact_integer_arithmetic():
    # XXX: re-fix this so that all operations are tested with all rounding modes
    random.seed(0)
    for prec in [6, 10, 25, 40, 100, 250, 725]:
        for rounding in ['d', 'u', 'f', 'c', 'n']:
            mp.dps = prec
            M = 10**(prec-2)
            M2 = 10**(prec//2-2)
            for i in range(10):
                a = random.randint(-M, M)
                b = random.randint(-M, M)
                assert mpf(a, rounding=rounding) == a
                assert int(mpf(a, rounding=rounding)) == a
                assert int(mpf(str(a), rounding=rounding)) == a
                assert mpf(a) + mpf(b) == a + b
                assert mpf(a) - mpf(b) == a - b
                assert -mpf(a) == -a
                a = random.randint(-M2, M2)
                b = random.randint(-M2, M2)
                assert mpf(a) * mpf(b) == a*b
                assert mpf_mul(from_int(a), from_int(b), mp.prec, rounding) == from_int(a*b)
    mp.dps = 15

