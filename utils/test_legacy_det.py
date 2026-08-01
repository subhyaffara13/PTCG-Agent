
def test_legacy_det(method, M, sol):
    # Minimal support for legacy keys for 'method' in det()
    # Partially copied from test_determinant()
    assert M.det(method=method) == sol

