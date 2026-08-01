
def test_evalpow_bug():
    x = Symbol("x")
    assert 1/(1/x) == x
    assert 1/(-1/x) == -x

