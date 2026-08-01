
def test_CircularOrthogonalEnsemble():
    CO = COE('U', 3)
    j, k = (Dummy('j', integer=True, positive=True),
            Dummy('k', integer=True, positive=True))
    t = IndexedBase('t')
    assert joint_eigen_distribution(CO).dummy_eq(
            Lambda((t[1], t[2], t[3]),
            Product(Abs(exp(I*t[j]) - exp(I*t[k])),
            (j, k + 1, 3), (k, 1, 2))/(48*pi**2))
    )

