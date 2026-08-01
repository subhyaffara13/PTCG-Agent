
def test_dup_cauchy_lower_bound():
    raises(PolynomialError, lambda: dup_cauchy_lower_bound([], QQ))
    raises(PolynomialError, lambda: dup_cauchy_lower_bound([QQ(1)], QQ))
    raises(PolynomialError, lambda: dup_cauchy_lower_bound([QQ(1), QQ(0), QQ(0)], QQ))
    raises(DomainError, lambda: dup_cauchy_lower_bound([ZZ_I(1), ZZ_I(1)], ZZ_I))

    assert dup_cauchy_lower_bound([QQ(1), QQ(0), QQ(-2)], QQ) == QQ(2, 3)

