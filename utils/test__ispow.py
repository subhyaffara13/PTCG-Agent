
def test__ispow():
    assert _ispow(x**2)
    assert not _ispow(x)
    assert not _ispow(True)

