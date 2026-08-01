
def test_LoweringOp():
    assert Dagger(a) == ad
    assert Commutator(a, ad).doit() == Integer(1)
    assert Commutator(a, N).doit() == a
    assert qapply(a*k) == (sqrt(k.n)*SHOKet(k.n-Integer(1))).expand()
    assert qapply(a*kz) == Integer(0)
    assert qapply(a*kf) == (sqrt(kf.n)*SHOKet(kf.n-Integer(1))).expand()
    assert a.rewrite('xp').doit() == \
        (Integer(1)/sqrt(Integer(2)*hbar*m*omega))*(I*Px + m*omega*X)
    for i in range(ndim - 1):
        assert a_rep[i,i + 1] == sqrt(i + 1)

