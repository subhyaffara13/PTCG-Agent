
def test_applyfunc():
    m0 = OperationsOnlyMatrix(eye(3))
    assert m0.applyfunc(lambda x: 2*x) == eye(3)*2
    assert m0.applyfunc(lambda x: 0) == zeros(3)
    assert m0.applyfunc(lambda x: 1) == ones(3)


def test_applyfunc():
    m0 = eye(3)
    assert m0.applyfunc(lambda x: 2*x) == eye(3)*2
    assert m0.applyfunc(lambda x: 0) == zeros(3)


def test_applyfunc():
    m0 = eye(3)
    assert m0.applyfunc(lambda x: 2*x) == eye(3)*2
    assert m0.applyfunc(lambda x: 0) == zeros(3)

