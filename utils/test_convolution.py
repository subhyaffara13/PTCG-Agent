
def test_convolution():
    # fft
    a = [1, Rational(5, 3), sqrt(3), Rational(7, 5)]
    b = [9, 5, 5, 4, 3, 2]
    c = [3, 5, 3, 7, 8]
    d = [1422, 6572, 3213, 5552]
    e = [-1, Rational(5, 3), Rational(7, 5)]

    assert convolution(a, b) == convolution_fft(a, b)
    assert convolution(a, b, dps=9) == convolution_fft(a, b, dps=9)
    assert convolution(a, d, dps=7) == convolution_fft(d, a, dps=7)
    assert convolution(a, d[1:], dps=3) == convolution_fft(d[1:], a, dps=3)

    # prime moduli of the form (m*2**k + 1), sequence length
    # should be a divisor of 2**k
    p = 7*17*2**23 + 1
    q = 19*2**10 + 1

    # ntt
    assert convolution(d, b, prime=q) == convolution_ntt(b, d, prime=q)
    assert convolution(c, b, prime=p) == convolution_ntt(b, c, prime=p)
    assert convolution(d, c, prime=p) == convolution_ntt(c, d, prime=p)
    raises(TypeError, lambda: convolution(b, d, dps=5, prime=q))
    raises(TypeError, lambda: convolution(b, d, dps=6, prime=q))

    # fwht
    assert convolution(a, b, dyadic=True) == convolution_fwht(a, b)
    assert convolution(a, b, dyadic=False) == convolution(a, b)
    raises(TypeError, lambda: convolution(b, d, dps=2, dyadic=True))
    raises(TypeError, lambda: convolution(b, d, prime=p, dyadic=True))
    raises(TypeError, lambda: convolution(a, b, dps=2, dyadic=True))
    raises(TypeError, lambda: convolution(b, c, prime=p, dyadic=True))

    # subset
    assert convolution(a, b, subset=True) == convolution_subset(a, b) == \
            convolution(a, b, subset=True, dyadic=False) == \
                convolution(a, b, subset=True)
    assert convolution(a, b, subset=False) == convolution(a, b)
    raises(TypeError, lambda: convolution(a, b, subset=True, dyadic=True))
    raises(TypeError, lambda: convolution(c, d, subset=True, dps=6))
    raises(TypeError, lambda: convolution(a, c, subset=True, prime=q))

    # integer
    assert convolution([0], [0]) == convolution_int([0], [0])
    assert convolution(b, c) == convolution_int(b, c)

    # rational
    assert convolution([Rational(1,2)], [Rational(1,2)]) == [Rational(1, 4)]
    assert convolution(b, e) == [-9, 10, Rational(239, 15), Rational(34, 3),
                                 Rational(32, 3), Rational(43, 5), Rational(113, 15),
                                 Rational(14, 5)]

