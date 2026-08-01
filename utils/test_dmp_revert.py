
def test_dmp_revert():
    f = [-QQ(1, 720), QQ(0), QQ(1, 24), QQ(0), -QQ(1, 2), QQ(0), QQ(1)]
    g = [QQ(61, 720), QQ(0), QQ(5, 24), QQ(0), QQ(1, 2), QQ(0), QQ(1)]

    assert dmp_revert(f, 8, 0, QQ) == g

    raises(MultivariatePolynomialError, lambda: dmp_revert([[1]], 2, 1, QQ))

