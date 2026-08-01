
def test_GaussianUnitaryEnsemble():
    H = RandomMatrixSymbol('H', 3, 3)
    G = GUE('U', 3)
    assert density(G)(H) == sqrt(2)*exp(-3*Trace(H**2)/2)/(4*pi**Rational(9, 2))
    i, j = (Dummy('i', integer=True, positive=True),
            Dummy('j', integer=True, positive=True))
    l = IndexedBase('l')
    assert joint_eigen_distribution(G).dummy_eq(
            Lambda((l[1], l[2], l[3]),
            27*sqrt(6)*exp(-3*(l[1]**2)/2 - 3*(l[2]**2)/2 - 3*(l[3]**2)/2)*
            Product(Abs(l[i] - l[j])**2, (j, i + 1, 3), (i, 1, 2))/(16*pi**Rational(3, 2))))
    s = Dummy('s')
    assert level_spacing_distribution(G).dummy_eq(Lambda(s, 32*s**2*exp(-4*s**2/pi)/pi**2))

