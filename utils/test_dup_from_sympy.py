
def test_dup_from_sympy():
    assert dup_from_sympy([S.One, S(2)], ZZ) == \
        [ZZ(1), ZZ(2)]
    assert dup_from_sympy([S.Half, S(3)], QQ) == \
        [QQ(1, 2), QQ(3, 1)]

