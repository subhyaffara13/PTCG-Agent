
def test_issue_20582():
    A = Matrix([
        [5, -5, -3, 2, -7],
        [-2, -5, 0, 2, 1],
        [-2, -7, -5, -2, -6],
        [7, 10, 3, 9, -2],
        [4, -10, 3, -8, -4]
    ])
    # XXX Used dry-run test because arbitrary symbol that appears in
    # CRootOf may not be unique.
    assert A.eigenvects()

