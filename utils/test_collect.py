
def test_collect():
    assert collect(A*B - B*A, A) == A*B - B*A
    assert collect(A*B - B*A, B) == A*B - B*A
    assert collect(A*B - B*A, x) == A*B - B*A

