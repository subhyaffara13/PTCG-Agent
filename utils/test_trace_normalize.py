
def test_trace_normalize():
    assert Trace(B*A) != Trace(A*B)
    assert Trace(B*A)._normalize() == Trace(A*B)
    assert Trace(B*A.T)._normalize() == Trace(A*B.T)

