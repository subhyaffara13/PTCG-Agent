
def test_zip_row_op():
    for cls in classes[:2]: # XXX: immutable matrices don't support row ops
        M = cls.eye(3)
        M.zip_row_op(1, 0, lambda v, u: v + 2*u)
        assert M == cls([[1, 0, 0],
                         [2, 1, 0],
                         [0, 0, 1]])

        M = cls.eye(3)*2
        M[0, 1] = -1
        M.zip_row_op(1, 0, lambda v, u: v + 2*u); M
        assert M == cls([[2, -1, 0],
                         [4,  0, 0],
                         [0,  0, 2]])


def test_zip_row_op():
    for cls in mutable_classes: # XXX: immutable matrices don't support row ops
        M = cls.eye(3)
        M.zip_row_op(1, 0, lambda v, u: v + 2*u)
        assert M == cls([[1, 0, 0],
                         [2, 1, 0],
                         [0, 0, 1]])

        M = cls.eye(3)*2
        M[0, 1] = -1
        M.zip_row_op(1, 0, lambda v, u: v + 2*u); M
        assert M == cls([[2, -1, 0],
                         [4,  0, 0],
                         [0,  0, 2]])

