
def test_DMP___bool__():
    assert bool(DMP([[]], ZZ)) is False
    assert bool(DMP([[ZZ(1)]], ZZ)) is True

