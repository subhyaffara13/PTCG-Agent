
def test_ANP___init__():
    rep = [QQ(1), QQ(1)]
    mod = [QQ(1), QQ(0), QQ(1)]

    f = ANP(rep, mod, QQ)

    assert f.to_list() == [QQ(1), QQ(1)]
    assert f.mod_to_list() == [QQ(1), QQ(0), QQ(1)]
    assert f.dom == QQ

    rep = {1: QQ(1), 0: QQ(1)}
    mod = {2: QQ(1), 0: QQ(1)}

    f = ANP(rep, mod, QQ)

    assert f.to_list() == [QQ(1), QQ(1)]
    assert f.mod_to_list() == [QQ(1), QQ(0), QQ(1)]
    assert f.dom == QQ

    f = ANP(1, mod, QQ)

    assert f.to_list() == [QQ(1)]
    assert f.mod_to_list() == [QQ(1), QQ(0), QQ(1)]
    assert f.dom == QQ

    f = ANP([1, 0.5], mod, QQ)

    assert all(QQ.of_type(a) for a in f.to_list())

    raises(CoercionFailed, lambda: ANP([sqrt(2)], mod, QQ))

