
def test_MatrixLinearOperator_refcycle(xp):
    # gh-10634
    # Test that MatrixLinearOperator can be automatically garbage collected
    A = xp.eye(2)
    with assert_deallocated(interface.MatrixLinearOperator, A, xp) as op:
        op.adjoint()
        del op

