
def test_trace_rewrite():
    assert trace(A).rewrite(Sum) == Sum(A[i, i], (i, 0, n - 1))
    assert trace(eye(3)).rewrite(Sum) == 3

