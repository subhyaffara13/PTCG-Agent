
def test_dup_monic():
    assert dup_monic([3, 6, 9], ZZ) == [1, 2, 3]

    raises(ExactQuotientFailed, lambda: dup_monic([3, 4, 5], ZZ))

    assert dup_monic([], QQ) == []
    assert dup_monic([QQ(1)], QQ) == [QQ(1)]
    assert dup_monic([QQ(7), QQ(1), QQ(21)], QQ) == [QQ(1), QQ(1, 7), QQ(3)]

