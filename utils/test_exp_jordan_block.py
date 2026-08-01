
def test_exp_jordan_block():
    l = Symbol('lamda')

    m = Matrix.jordan_block(1, l)
    assert m._eval_matrix_exp_jblock() == Matrix([[exp(l)]])

    m = Matrix.jordan_block(3, l)
    assert m._eval_matrix_exp_jblock() == \
        Matrix([
            [exp(l), exp(l), exp(l)/2],
            [0, exp(l), exp(l)],
            [0, 0, exp(l)]])


def test_exp_jordan_block():
    l = Symbol('lamda')

    m = Matrix.jordan_block(1, l)
    assert m._eval_matrix_exp_jblock() == Matrix([[exp(l)]])

    m = Matrix.jordan_block(3, l)
    assert m._eval_matrix_exp_jblock() == \
        Matrix([
            [exp(l), exp(l), exp(l)/2],
            [0, exp(l), exp(l)],
            [0, 0, exp(l)]])

