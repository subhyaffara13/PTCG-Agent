
def test_P6():
    M = Matrix([[cos(x), sin(x)],
                [-sin(x), cos(x)]])
    assert M.diff(x, 2) == Matrix([[-cos(x), -sin(x)],
                                   [sin(x), -cos(x)]])

