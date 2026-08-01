
def test_issue_10770():
    M = Matrix([])
    a = ['col_insert', 'row_join'], Matrix([9, 6, 3])
    b = ['row_insert', 'col_join'], a[1].T
    c = ['row_insert', 'col_insert'], Matrix([[1, 2], [3, 4]])
    for ops, m in (a, b, c):
        for op in ops:
            f = getattr(M, op)
            new = f(m) if 'join' in op else f(42, m)
            assert new == m and id(new) != id(m)


def test_issue_10770():
    M = Matrix([])
    a = ['col_insert', 'row_join'], Matrix([9, 6, 3])
    b = ['row_insert', 'col_join'], a[1].T
    c = ['row_insert', 'col_insert'], Matrix([[1, 2], [3, 4]])
    for ops, m in (a, b, c):
        for op in ops:
            f = getattr(M, op)
            new = f(m) if 'join' in op else f(42, m)
            assert new == m and id(new) != id(m)

