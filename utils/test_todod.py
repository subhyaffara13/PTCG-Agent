
def test_todod():
    m = ShapingOnlyMatrix(3, 2, [[S.One, 0], [0, S.Half], [x, 0]])
    dict = {0: {0: S.One}, 1: {1: S.Half}, 2: {0: x}}
    assert m.todod() == dict


def test_todod():
    m = Matrix([[S.One, 0], [0, S.Half], [x, 0]])
    dict = {0: {0: S.One}, 1: {1: S.Half}, 2: {0: x}}
    assert m.todod() == dict

