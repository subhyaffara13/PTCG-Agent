
def test_P45():
    def __my_wronskian(Y, v):
        M = Matrix([Matrix(Y).T.diff(x, n) for n in range(0, len(Y))])
        return  M.det()
    assert __my_wronskian([cos(x), sin(x)], x).simplify() == 1

