
def test_interval_matrix_mult_bug():
    # regression test for interval matrix multiplication:
    # result must be nonzero-width and contain the exact result
    x = convert('1.00000000000001') # note: this is implicitly rounded to some near mpf float value
    A = matrix([[x]])
    B = iv.matrix(A)
    C = iv.matrix([[x]])
    assert B == C
    B = B * B
    C = C * C
    assert B == C
    assert B[0, 0].delta > 1e-16
    assert B[0, 0].delta < 3e-16
    assert C[0, 0].delta > 1e-16
    assert C[0, 0].delta < 3e-16
    assert mp.mpf('1.00000000000001998401444325291756783368705994138804689654') in B[0, 0]
    assert mp.mpf('1.00000000000001998401444325291756783368705994138804689654') in C[0, 0]
    # the following caused an error before the bug was fixed
    assert iv.matrix(mp.eye(2)) * (iv.ones(2) + mpi(1, 2)) == iv.matrix([[mpi(2, 3), mpi(2, 3)], [mpi(2, 3), mpi(2, 3)]])

