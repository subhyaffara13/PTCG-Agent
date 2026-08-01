
def test_local():
    igrlex = InverseOrder(grlex)
    gens = [x, y, z]

    def contains(I, f):
        S = [sdm_from_vector([g], igrlex, QQ, gens=gens) for g in I]
        G = sdm_groebner(S, sdm_nf_mora, igrlex, QQ)
        return sdm_nf_mora(sdm_from_vector([f], lex, QQ, gens=gens),
                           G, lex, QQ) == sdm_zero()
    assert contains([x, y], x)
    assert contains([x, y], x + y)
    assert not contains([x, y], 1)
    assert not contains([x, y], z)
    assert contains([x**2 + y, x**2 + x], x - y)
    assert not contains([x + y + z, x*y + x*z + y*z, x*y*z], x**2)
    assert contains([x*(1 + x + y), y*(1 + z)], x)
    assert contains([x*(1 + x + y), y*(1 + z)], x + y)


def test_local(test):
    _test_factory(test)

