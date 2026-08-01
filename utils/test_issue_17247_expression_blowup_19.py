
def test_issue_17247_expression_blowup_19():
    M = Matrix(S('''[
        [             -3/4,                     0,         1/4 + I/2,                     0],
        [                0, -177/128 - 1369*I/128,                 0, -2063/256 + 541*I/128],
        [          1/2 - I,                     0,                 0,                     0],
        [                0,                     0,                 0, -177/128 - 1369*I/128]]'''))
    with dotprodsimp(True):
        assert not M.is_diagonalizable()


def test_issue_17247_expression_blowup_19():
    M = Matrix(S('''[
        [             -3/4,                     0,         1/4 + I/2,                     0],
        [                0, -177/128 - 1369*I/128,                 0, -2063/256 + 541*I/128],
        [          1/2 - I,                     0,                 0,                     0],
        [                0,                     0,                 0, -177/128 - 1369*I/128]]'''))
    with dotprodsimp(True):
        assert not M.is_diagonalizable()

