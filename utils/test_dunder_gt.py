
def test_dunder_gt(A, Asp):
    assert not (Asp > Asp).toarray().any()
    assert not (A > Asp).any()

