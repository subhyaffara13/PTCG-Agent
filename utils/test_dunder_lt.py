
def test_dunder_lt(A, Asp):
    assert not (Asp < Asp).toarray().any()
    assert not (A < Asp).any()

