
def test_dot():
    v1 = C.x * i + C.z * C.z * j
    v2 = C.x * i + C.y * j + C.z * k
    assert Dot(v1, v2) == Dot(C.x*C.i + C.z**2*C.j, C.x*C.i + C.y*C.j + C.z*C.k)
    assert Dot(v1, v2).doit() == C.x**2 + C.y*C.z**2
    assert Dot(v2, v1).doit() == C.x**2 + C.y*C.z**2
    assert Dot(v1, v2) == Dot(v2, v1)


def test_dot():
    assert dot(A.x, A.x) == 1
    assert dot(A.x, A.y) == 0
    assert dot(A.x, A.z) == 0

    assert dot(A.y, A.x) == 0
    assert dot(A.y, A.y) == 1
    assert dot(A.y, A.z) == 0

    assert dot(A.z, A.x) == 0
    assert dot(A.z, A.y) == 0
    assert dot(A.z, A.z) == 1


def test_dot():
    assert ones(1, 3).dot(ones(3, 1)) == 3
    assert ones(1, 3).dot([1, 1, 1]) == 3
    assert Matrix([1, 2, 3]).dot(Matrix([1, 2, 3])) == 14
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I])) == -5 + I
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I]), hermitian=False) == -5 + I
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I]), hermitian=True) == 13 + I
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I]), hermitian=True, conjugate_convention="physics") == 13 - I
    assert Matrix([1, 2, 3*I]).dot(Matrix([4, 5*I, 6]), hermitian=True, conjugate_convention="right") == 4 + 8*I
    assert Matrix([1, 2, 3*I]).dot(Matrix([4, 5*I, 6]), hermitian=True, conjugate_convention="left") == 4 - 8*I
    assert Matrix([I, 2*I]).dot(Matrix([I, 2*I]), hermitian=False, conjugate_convention="left") == -5
    assert Matrix([I, 2*I]).dot(Matrix([I, 2*I]), conjugate_convention="left") == 5
    raises(ValueError, lambda: Matrix([1, 2]).dot(Matrix([3, 4]), hermitian=True, conjugate_convention="test"))


def test_dot():
    assert ones(1, 3).dot(ones(3, 1)) == 3
    assert ones(1, 3).dot([1, 1, 1]) == 3
    assert Matrix([1, 2, 3]).dot(Matrix([1, 2, 3])) == 14
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I])) == -5 + I
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I]), hermitian=False) == -5 + I
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I]), hermitian=True) == 13 + I
    assert Matrix([1, 2, 3*I]).dot(Matrix([I, 2, 3*I]), hermitian=True, conjugate_convention="physics") == 13 - I
    assert Matrix([1, 2, 3*I]).dot(Matrix([4, 5*I, 6]), hermitian=True, conjugate_convention="right") == 4 + 8*I
    assert Matrix([1, 2, 3*I]).dot(Matrix([4, 5*I, 6]), hermitian=True, conjugate_convention="left") == 4 - 8*I
    assert Matrix([I, 2*I]).dot(Matrix([I, 2*I]), hermitian=False, conjugate_convention="left") == -5
    assert Matrix([I, 2*I]).dot(Matrix([I, 2*I]), conjugate_convention="left") == 5
    raises(ValueError, lambda: Matrix([1, 2]).dot(Matrix([3, 4]), hermitian=True, conjugate_convention="test"))


def test_dot():
    raises(TypeError, lambda: Point(1, 2).dot(Line((0, 0), (1, 1))))

