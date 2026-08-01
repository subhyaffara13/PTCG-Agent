
def test_QQ_int():
    assert int(QQ(2**2000, 3**1250)) == 455431
    assert int(QQ(2**100, 3)) == 422550200076076467165567735125

