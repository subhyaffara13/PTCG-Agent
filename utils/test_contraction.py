
def test_contraction():
    i, j, k, l = symbols('i,j,k,l', below_fermi=True)
    a, b, c, d = symbols('a,b,c,d', above_fermi=True)
    p, q, r, s = symbols('p,q,r,s')
    assert contraction(Fd(i), F(j)) == KroneckerDelta(i, j)
    assert contraction(F(a), Fd(b)) == KroneckerDelta(a, b)
    assert contraction(F(a), Fd(i)) == 0
    assert contraction(Fd(a), F(i)) == 0
    assert contraction(F(i), Fd(a)) == 0
    assert contraction(Fd(i), F(a)) == 0
    assert contraction(Fd(i), F(p)) == KroneckerDelta(i, p)
    restr = evaluate_deltas(contraction(Fd(p), F(q)))
    assert restr.is_only_below_fermi
    restr = evaluate_deltas(contraction(F(p), Fd(q)))
    assert restr.is_only_above_fermi
    raises(ContractionAppliesOnlyToFermions, lambda: contraction(B(a), Fd(b)))

