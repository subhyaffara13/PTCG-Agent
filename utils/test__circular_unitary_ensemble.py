
def test_CircularUnitaryEnsemble():
    CU = CUE('U', 3)
    j, k = (Dummy('j', integer=True, positive=True),
            Dummy('k', integer=True, positive=True))
    t = IndexedBase('t')
    assert joint_eigen_distribution(CU).dummy_eq(
            Lambda((t[1], t[2], t[3]),
            Product(Abs(exp(I*t[j]) - exp(I*t[k]))**2,
            (j, k + 1, 3), (k, 1, 2))/(48*pi**3))
    )

