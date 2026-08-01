
def test_ref_qualified():
    """Tests that explicit lvalue ref-qualified methods can be called just like their
    non ref-qualified counterparts."""

    r = m.RefQualified()
    assert r.value == 0
    r.refQualified(17)
    assert r.value == 17
    assert r.constRefQualified(23) == 40

