
def test_canonical_unit():

    for K in [ZZ, QQ, RR]: # CC?
        assert K.canonical_unit(K(2)) == K(1)
        assert K.canonical_unit(K(-2)) == K(-1)

    for K in [ZZ_I, QQ_I]:
        i = K.from_sympy(I)
        assert K.canonical_unit(K(2)) == K(1)
        assert K.canonical_unit(K(2)*i) == -i
        assert K.canonical_unit(-K(2)) == K(-1)
        assert K.canonical_unit(-K(2)*i) == i

    K = ZZ[x]
    assert K.canonical_unit(K(x + 1)) == K(1)
    assert K.canonical_unit(K(-x + 1)) == K(-1)

    K = ZZ_I[x]
    assert K.canonical_unit(K.from_sympy(I*x)) == ZZ_I(0, -1)

    K = ZZ_I.frac_field(x, y)
    i = K.from_sympy(I)
    assert i / i == K.one
    assert (K.one + i)/(i - K.one) == -i

