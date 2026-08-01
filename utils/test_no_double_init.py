
def test_no_double_init(xp):
    call_count = [0]

    def matvec(v):
        call_count[0] += 1
        return v

    # It should call matvec exactly once (in order to determine the
    # operator dtype)
    interface.LinearOperator((2, 2), matvec=matvec, xp=xp)
    assert_equal(call_count[0], 1)

