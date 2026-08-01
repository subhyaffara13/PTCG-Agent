
def test_casts_none():
    """#2778: implicit casting from None to object (not pointer)"""
    a = m.NoneCastTester()
    assert m.ok_obj_or_none(a) == -1
    a = m.NoneCastTester(4)
    assert m.ok_obj_or_none(a) == 4
    a = m.NoneCastTester(None)
    assert m.ok_obj_or_none(a) == -1
    assert m.ok_obj_or_none(None) == -1

