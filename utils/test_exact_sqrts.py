import random

def test_exact_sqrts():
    for i in range(20000):
        assert sqrt(mpf(i*i)) == i
    random.seed(1)
    for prec in [100, 300, 1000, 10000]:
        mp.dps = prec
        for i in range(20):
            A = random.randint(10**(prec//2-2), 10**(prec//2-1))
            assert sqrt(mpf(A*A)) == A
    mp.dps = 15
    for i in range(100):
        for a in [1, 8, 25, 112307]:
            assert sqrt(mpf((a*a, 2*i))) == mpf((a, i))
            assert sqrt(mpf((a*a, -2*i))) == mpf((a, -i))

