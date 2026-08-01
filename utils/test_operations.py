
def test_operations():
    per = SeqPer((1, 2), (n, 0, oo))
    per2 = SeqPer((2, 4), (n, 0, oo))
    form = SeqFormula(n**2)
    form2 = SeqFormula(n**3)

    assert per + form + form2 == SeqAdd(per, form, form2)
    assert per + form - form2 == SeqAdd(per, form, -form2)
    assert per + form - S.EmptySequence == SeqAdd(per, form)
    assert per + per2 + form == SeqAdd(SeqPer((3, 6), (n, 0, oo)), form)
    assert S.EmptySequence - per == -per
    assert form + form == SeqFormula(2*n**2)

    assert per * form * form2 == SeqMul(per, form, form2)
    assert form * form == SeqFormula(n**4)
    assert form * -form == SeqFormula(-n**4)

    assert form * (per + form2) == SeqMul(form, SeqAdd(per, form2))
    assert form * (per + per) == SeqMul(form, per2)

    assert form.coeff_mul(m) == SeqFormula(m*n**2, (n, 0, oo))
    assert per.coeff_mul(m) == SeqPer((m, 2*m), (n, 0, oo))


def test_operations():
    F = QQ.old_poly_ring(x).free_module(2)
    G = QQ.old_poly_ring(x).free_module(3)
    f = F.identity_hom()
    g = homomorphism(F, F, [0, [1, x]])
    h = homomorphism(F, F, [[1, 0], 0])
    i = homomorphism(F, G, [[1, 0, 0], [0, 1, 0]])

    assert f == f
    assert f != g
    assert f != i
    assert (f != F.identity_hom()) is False
    assert 2*f == f*2 == homomorphism(F, F, [[2, 0], [0, 2]])
    assert f/2 == homomorphism(F, F, [[S.Half, 0], [0, S.Half]])
    assert f + g == homomorphism(F, F, [[1, 0], [1, x + 1]])
    assert f - g == homomorphism(F, F, [[1, 0], [-1, 1 - x]])
    assert f*g == g == g*f
    assert h*g == homomorphism(F, F, [0, [1, 0]])
    assert g*h == homomorphism(F, F, [0, 0])
    assert i*f == i
    assert f([1, 2]) == [1, 2]
    assert g([1, 2]) == [2, 2*x]

    assert i.restrict_domain(F.submodule([x, x]))([x, x]) == i([x, x])
    h1 = h.quotient_domain(F.submodule([0, 1]))
    assert h1([1, 0]) == h([1, 0])
    assert h1.restrict_domain(h1.domain.submodule([x, 0]))([x, 0]) == h([x, 0])

    raises(TypeError, lambda: f/g)
    raises(TypeError, lambda: f + 1)
    raises(TypeError, lambda: f + i)
    raises(TypeError, lambda: f - 1)
    raises(TypeError, lambda: f*i)

