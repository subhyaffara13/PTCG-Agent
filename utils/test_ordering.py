
def test_ordering():
    signatures = [[A, A], [A, B], [B, A], [B, B], [A, C]]
    ord = ordering(signatures)
    assert ord[0] == (B, B) or ord[0] == (A, C)
    assert ord[-1] == (A, A) or ord[-1] == (A, C)


def test_ordering(python_version_mock):
    assert evaluate_marker("python_full_version > '2.7.3'") is True

