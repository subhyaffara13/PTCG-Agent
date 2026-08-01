
def test_uncovered_line():
    gens = [x, y]
    f1 = sdm_zero()
    f2 = sdm_from_vector([x, 0], lex, QQ, gens=gens)
    f3 = sdm_from_vector([0, y], lex, QQ, gens=gens)

    assert sdm_spoly(f1, f2, lex, QQ) == sdm_zero()
    assert sdm_spoly(f3, f2, lex, QQ) == sdm_zero()

