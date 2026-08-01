
def test_states():
    d = Density([Ket(0), 0.5], [Ket(1), 0.5])
    states = d.states()
    assert states[0] == Ket(0) and states[1] == Ket(1)


def test_states():
    assert PIABKet(n).dual_class() == PIABBra
    assert PIABKet(n).hilbert_space == \
        L2(Interval(S.NegativeInfinity, S.Infinity))
    assert represent(PIABKet(n)) == sqrt(2/L)*sin(n*pi*x/L)
    assert (PIABBra(i)*PIABKet(j)).doit() == KroneckerDelta(i, j)
    assert PIABBra(n).dual_class() == PIABKet

