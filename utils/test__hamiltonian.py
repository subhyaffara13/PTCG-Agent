
def test_Hamiltonian():
    assert Commutator(H, N).doit() == Integer(0)
    assert qapply(H*k) == ((hbar*omega*(k.n + Integer(1)/Integer(2)))*k).expand()
    assert H.rewrite('a').doit() == hbar*omega*(ad*a + Integer(1)/Integer(2))
    assert H.rewrite('xp').doit() == \
        (Integer(1)/(Integer(2)*m))*(Px**2 + (m*omega*X)**2)
    assert H.rewrite('N').doit() == hbar*omega*(N + Integer(1)/Integer(2))
    for i in range(ndim):
        assert H_rep[i,i] == hbar*omega*(i + Integer(1)/Integer(2))

