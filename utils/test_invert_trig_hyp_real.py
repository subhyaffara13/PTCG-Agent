
def test_invert_trig_hyp_real():
    # check some codepaths that are not as easily reached otherwise
    n = Dummy('n')
    assert _invert_trig_hyp_real(cosh(x), Range(-5, 10, 1), x)[1].dummy_eq(Union(
        ImageSet(Lambda(n, -acosh(n)), Range(1, 10, 1)),
        ImageSet(Lambda(n, acosh(n)), Range(1, 10, 1))))
    assert _invert_trig_hyp_real(coth(x), Interval(-3, 2), x) == (x, Union(
        Interval(-oo, -acoth(3)), Interval(acoth(2), oo)))
    assert _invert_trig_hyp_real(tanh(x), Interval(-S.Half, 1), x) == (x,
        Interval(-atanh(S.Half), oo))
    assert _invert_trig_hyp_real(sech(x), imageset(n, S.Half + n/3, S.Naturals0), x) == \
        (x, FiniteSet(-asech(S(1)/2), asech(S(1)/2), -asech(S(5)/6), asech(S(5)/6)))
    assert _invert_trig_hyp_real(csch(x), S.Reals, x) == (x,
        Union(Interval.open(-oo, 0), Interval.open(0, oo)))

