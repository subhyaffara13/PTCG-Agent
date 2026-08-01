
def test_igcd_lehmer():
    a, b = fibonacci(10001), fibonacci(10000)
    # len(str(a)) == 2090
    # small divisors, long Euclidean sequence
    assert igcd_lehmer(a, b) == 1
    c = fibonacci(100)
    assert igcd_lehmer(a*c, b*c) == c
    # big divisor
    assert igcd_lehmer(a, 10**1000) == 1
    # swapping argument
    assert igcd_lehmer(1, 2) == igcd_lehmer(2, 1)

