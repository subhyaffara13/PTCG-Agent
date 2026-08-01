
def test_dup_revert():
    f = [-QQ(1, 720), QQ(0), QQ(1, 24), QQ(0), -QQ(1, 2), QQ(0), QQ(1)]
    g = [QQ(61, 720), QQ(0), QQ(5, 24), QQ(0), QQ(1, 2), QQ(0), QQ(1)]

    assert dup_revert(f, 8, QQ) == g

    raises(NotReversible, lambda: dup_revert([QQ(1), QQ(0)], 3, QQ))

