
def test_mul__coeff_mul():
    assert SeqPer((1, 2), (n, 0, oo)).coeff_mul(2) == SeqPer((2, 4), (n, 0, oo))
    assert SeqFormula(n**2).coeff_mul(2) == SeqFormula(2*n**2)
    assert S.EmptySequence.coeff_mul(100) == S.EmptySequence

    assert SeqPer((1, 2), (n, 0, oo)) * (SeqPer((2, 3))) == \
        SeqPer((2, 6), (n, 0, oo))
    assert SeqFormula(n**2) * SeqFormula(n**3) == SeqFormula(n**5)

    assert S.EmptySequence * SeqFormula(n**2) == S.EmptySequence
    assert SeqFormula(n**2) * S.EmptySequence == S.EmptySequence

    raises(TypeError, lambda: sequence(n**2) * n)
    raises(TypeError, lambda: n * sequence(n**2))

