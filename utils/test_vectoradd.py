
def test_vectoradd():
    assert isinstance(Add(C.i, C.j), VectorAdd)
    v1 = C.x * i + C.z * C.z * j
    v2 = C.x * i + C.y * j + C.z * k
    assert isinstance(Add(v1, v2), VectorAdd)

    # https://github.com/sympy/sympy/issues/26121

    E = Matrix([C.i, C.j, C.k]).T
    a = Matrix([1, 2, 3])
    av = E*a

    assert av[0].kind == VectorKind()
    assert isinstance(av[0], VectorAdd)

