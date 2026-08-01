
def test_NumberOp():
    assert Commutator(N, ad).doit() == ad
    assert Commutator(N, a).doit() == Integer(-1)*a
    assert Commutator(N, H).doit() == Integer(0)
    assert qapply(N*k) == (k.n*k).expand()
    assert N.rewrite('a').doit() == ad*a
    assert N.rewrite('xp').doit() == (Integer(1)/(Integer(2)*m*hbar*omega))*(
        Px**2 + (m*omega*X)**2) - Integer(1)/Integer(2)
    assert N.rewrite('H').doit() == H/(hbar*omega) - Integer(1)/Integer(2)
    for i in range(ndim):
        assert N_rep[i,i] == i
    assert N_rep == ad_rep_sympy*a_rep

