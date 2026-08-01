
def test_dup_cauchy_upper_bound():
    raises(PolynomialError, lambda: dup_cauchy_upper_bound([], QQ))
    raises(PolynomialError, lambda: dup_cauchy_upper_bound([QQ(1)], QQ))
    raises(DomainError, lambda: dup_cauchy_upper_bound([ZZ_I(1), ZZ_I(1)], ZZ_I))

    assert dup_cauchy_upper_bound([QQ(1), QQ(0), QQ(0)], QQ) == QQ.zero
    assert dup_cauchy_upper_bound([QQ(1), QQ(0), QQ(-2)], QQ) == QQ(3)

