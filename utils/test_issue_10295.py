
def test_issue_10295():
    if not numpy:
        skip("numpy not installed.")

    A = numpy.array([[1, 3, -1],
                     [0, 1, 7]])
    sA = S(A)
    assert sA.shape == (2, 3)
    for (ri, ci), val in numpy.ndenumerate(A):
        assert sA[ri, ci] == val

    B = numpy.array([-7, x, 3*y**2])
    sB = S(B)
    assert sB.shape == (3,)
    assert B[0] == sB[0] == -7
    assert B[1] == sB[1] == x
    assert B[2] == sB[2] == 3*y**2

    C = numpy.arange(0, 24)
    C.resize(2,3,4)
    sC = S(C)
    assert sC[0, 0, 0].is_integer
    assert sC[0, 0, 0] == 0

    a1 = numpy.array([1, 2, 3])
    a2 = numpy.array(list(range(24)))
    a2.resize(2, 4, 3)
    assert sympify(a1) == ImmutableDenseNDimArray([1, 2, 3])
    assert sympify(a2) == ImmutableDenseNDimArray(list(range(24)), (2, 4, 3))

