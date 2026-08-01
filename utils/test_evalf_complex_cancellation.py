
def test_evalf_complex_cancellation():
    A = Rational('63287/100000')
    B = Rational('52498/100000')
    C = Rational('69301/100000')
    D = Rational('83542/100000')
    F = Rational('2231321613/2500000000')
    # XXX: the number of returned mantissa digits in the real part could
    # change with the implementation. What matters is that the returned digits are
    # correct; those that are showing now are correct.
    # >>> ((A+B*I)*(C+D*I)).expand()
    # 64471/10000000000 + 2231321613*I/2500000000
    # >>> 2231321613*4
    # 8925286452L
    assert NS((A + B*I)*(C + D*I), 6) == '6.44710e-6 + 0.892529*I'
    assert NS((A + B*I)*(C + D*I), 10) == '6.447100000e-6 + 0.8925286452*I'
    assert NS((A + B*I)*(
        C + D*I) - F*I, 5) in ('6.4471e-6 + 0.e-14*I', '6.4471e-6 - 0.e-14*I')

