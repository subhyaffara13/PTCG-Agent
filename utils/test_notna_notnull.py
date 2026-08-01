
def test_notna_notnull(notna_f):
    assert notna_f(1.0)
    assert not notna_f(None)
    assert not notna_f(np.nan)

