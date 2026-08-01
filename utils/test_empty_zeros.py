
def test_empty_zeros():
    a = zeros(0)
    assert a == Matrix()
    a = zeros(0, 2)
    assert a.rows == 0
    assert a.cols == 2
    a = zeros(2, 0)
    assert a.rows == 2
    assert a.cols == 0


def test_empty_zeros():
    a = zeros(0)
    assert a == Matrix()
    a = zeros(0, 2)
    assert a.rows == 0
    assert a.cols == 2
    a = zeros(2, 0)
    assert a.rows == 2
    assert a.cols == 0

