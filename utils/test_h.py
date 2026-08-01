
def test_H():
    X = Normal('X', 0, 1)
    D = Die('D', sides = 4)
    G = Geometric('G', 0.5)
    assert H(X, X > 0) == -log(2)/2 + S.Half + log(pi)/2
    assert H(D, D > 2) == log(2)
    assert comp(H(G).evalf().round(2), 1.39)


def test_H():
    assert PIABHamiltonian('H').hilbert_space == \
        L2(Interval(S.NegativeInfinity, S.Infinity))
    assert qapply(PIABHamiltonian('H')*PIABKet(n)) == \
        (n**2*pi**2*hbar**2)/(2*m*L**2)*PIABKet(n)

