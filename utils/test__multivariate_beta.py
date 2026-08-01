
def test_MultivariateBeta():
    a1, a2 = symbols('a1, a2', positive=True)
    a1_f, a2_f = symbols('a1, a2', positive=False, real=True)
    mb = MultivariateBeta('B', [a1, a2])
    mb_c = MultivariateBeta('C', a1, a2)
    assert density(mb)(1, 2) == S(2)**(a2 - 1)*gamma(a1 + a2)/\
                                (gamma(a1)*gamma(a2))
    assert marginal_distribution(mb_c, 0)(3) == S(3)**(a1 - 1)*gamma(a1 + a2)/\
                                                (a2*gamma(a1)*gamma(a2))
    raises(ValueError, lambda: MultivariateBeta('b1', [a1_f, a2]))
    raises(ValueError, lambda: MultivariateBeta('b2', [a1, a2_f]))
    raises(ValueError, lambda: MultivariateBeta('b3', [0, 0]))
    raises(ValueError, lambda: MultivariateBeta('b4', [a1_f, a2_f]))
    assert mb.pspace.distribution.set == ProductSet(Interval(0, 1), Interval(0, 1))

