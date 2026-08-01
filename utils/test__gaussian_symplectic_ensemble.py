
def test_GaussianSymplecticEnsemble():
    H = RandomMatrixSymbol('H', 3, 3)
    _H = MatrixSymbol('_H', 3, 3)
    G = GSE('O', 3)
    assert density(G)(H) == exp(-3*Trace(H**2))/Integral(exp(-3*Trace(_H**2)), _H)
    i, j = (Dummy('i', integer=True, positive=True),
            Dummy('j', integer=True, positive=True))
    l = IndexedBase('l')
    assert joint_eigen_distribution(G).dummy_eq(
            Lambda((l[1], l[2], l[3]),
            162*sqrt(3)*exp(-3*l[1]**2/2 - 3*l[2]**2/2 - 3*l[3]**2/2)*
            Product(Abs(l[i] - l[j])**4, (j, i + 1, 3), (i, 1, 2))/(5*pi**Rational(3, 2))))
    s = Dummy('s')
    assert level_spacing_distribution(G).dummy_eq(Lambda(s, S(262144)*s**4*exp(-64*s**2/(9*pi))/(729*pi**3)))

