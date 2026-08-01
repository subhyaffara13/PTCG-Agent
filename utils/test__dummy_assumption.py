
def test_Dummy_assumption():
    d = Dummy('d', nonzero=True)
    assert d == eval(srepr(d))
    s1 = "Dummy('d', dummy_index=%s, nonzero=True)" % str(d.dummy_index)
    s2 = "Dummy('d', nonzero=True, dummy_index=%s)" % str(d.dummy_index)
    assert srepr(d) in (s1, s2)

