
def test_Dummy():
    d = Dummy('d')
    sT(d, "Dummy('d', dummy_index=%s)" % str(d.dummy_index))


def test_Dummy():
    assert str(d) == "_d"
    assert str(d + x) == "_d + x"


def test_Dummy():
    assert Dummy() != Dummy()

