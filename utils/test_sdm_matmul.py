
def test_SDM_matmul():
    A = SDM({0:{0:ZZ(2)}}, (2, 2), ZZ)
    B = SDM({0:{0:ZZ(4)}}, (2, 2), ZZ)
    assert A.matmul(A) == A*A == B

    C = SDM({0:{0:ZZ(2)}}, (2, 2), QQ)
    raises(DMDomainError, lambda: A.matmul(C))

    A = SDM({0:{0:ZZ(1), 1:ZZ(2)}, 1:{0:ZZ(3), 1:ZZ(4)}}, (2, 2), ZZ)
    B = SDM({0:{0:ZZ(7), 1:ZZ(10)}, 1:{0:ZZ(15), 1:ZZ(22)}}, (2, 2), ZZ)
    assert A.matmul(A) == A*A == B

    A22 = SDM({0:{0:ZZ(4)}}, (2, 2), ZZ)
    A32 = SDM({0:{0:ZZ(2)}}, (3, 2), ZZ)
    A23 = SDM({0:{0:ZZ(4)}}, (2, 3), ZZ)
    A33 = SDM({0:{0:ZZ(8)}}, (3, 3), ZZ)
    A22 = SDM({0:{0:ZZ(8)}}, (2, 2), ZZ)
    assert A32.matmul(A23) == A33
    assert A23.matmul(A32) == A22
    # XXX: @ not supported by SDM...
    #assert A32.matmul(A23) == A32 @ A23 == A33
    #assert A23.matmul(A32) == A23 @ A32 == A22
    #raises(DMShapeError, lambda: A23 @ A22)
    raises(DMShapeError, lambda: A23.matmul(A22))

    A = SDM({0: {0: ZZ(-1), 1: ZZ(1)}}, (1, 2), ZZ)
    B = SDM({0: {0: ZZ(-1)}, 1: {0: ZZ(-1)}}, (2, 1), ZZ)
    assert A.matmul(B) == A*B == SDM({}, (1, 1), ZZ)

