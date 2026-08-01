
def test_special_denom():
    # TODO: add more tests here
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t, t)]})
    assert special_denom(Poly(1, t), Poly(t**2, t), Poly(1, t), Poly(t**2 - 1, t),
    Poly(t, t), DE) == \
        (Poly(1, t), Poly(t**2 - 1, t), Poly(t**2 - 1, t), Poly(t, t))
#    assert special_denom(Poly(1, t), Poly(2*x, t), Poly((1 + 2*x)*t, t), DE) == 1

    # issue 3940
    # Note, this isn't a very good test, because the denominator is just 1,
    # but at least it tests the exp cancellation case
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(-2*x*t0, t0),
        Poly(I*k*t1, t1)]})
    DE.decrement_level()
    assert special_denom(Poly(1, t0), Poly(I*k, t0), Poly(1, t0), Poly(t0, t0),
    Poly(1, t0), DE) == \
        (Poly(1, t0, domain='ZZ'), Poly(I*k, t0, domain='ZZ_I[k,x]'),
                Poly(t0, t0, domain='ZZ'), Poly(1, t0, domain='ZZ'))


    assert special_denom(Poly(1, t), Poly(t**2, t), Poly(1, t), Poly(t**2 - 1, t),
    Poly(t, t), DE, case='tan') == \
           (Poly(1, t, t0, domain='ZZ'), Poly(t**2, t0, t, domain='ZZ[x]'),
            Poly(t, t, t0, domain='ZZ'), Poly(1, t0, domain='ZZ'))

    raises(ValueError, lambda: special_denom(Poly(1, t), Poly(t**2, t), Poly(1, t), Poly(t**2 - 1, t),
    Poly(t, t), DE, case='unrecognized_case'))

