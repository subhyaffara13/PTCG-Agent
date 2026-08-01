
def test_dunder_iter(A, Asp):
    assert all((a == asp).all() for a, asp in zip(A, Asp))

