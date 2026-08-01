
def test_special_matrices():
    assert julia_code(6*Identity(3)) == "6 * eye(3)"


def test_special_matrices():
    assert maple_code(6 * Identity(3)) == "6*Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]], storage = sparse)"
    assert maple_code(Identity(x)) == 'Matrix(x, shape = identity)'


def test_special_matrices():
    assert mcode(6*Identity(3)) == "6*eye(3)"

