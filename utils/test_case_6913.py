
def test_case_6913():
    m = MatrixSymbol('m', 1, 1)
    a = Symbol("a")
    a = m[0, 0]>0
    assert str(a) == 'm[0, 0] > 0'


def test_case_6913():
    m = MatrixSymbol('m', 1, 1)
    a = Symbol("a")
    a = m[0, 0]>0
    assert str(a) == 'm[0, 0] > 0'

