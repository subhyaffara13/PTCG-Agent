
def test_dunder_ne(A, Asp):
    assert not (Asp != Asp).toarray().any()
    assert not (A != Asp).any()

