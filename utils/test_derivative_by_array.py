
def test_derivative_by_array():
    from sympy.abc import i, j, t, x, y, z

    bexpr = x*y**2*exp(z)*log(t)
    sexpr = sin(bexpr)
    cexpr = cos(bexpr)

    a = Array([sexpr])

    assert derive_by_array(sexpr, t) == x*y**2*exp(z)*cos(x*y**2*exp(z)*log(t))/t
    assert derive_by_array(sexpr, [x, y, z]) == Array([bexpr/x*cexpr, 2*y*bexpr/y**2*cexpr, bexpr*cexpr])
    assert derive_by_array(a, [x, y, z]) == Array([[bexpr/x*cexpr], [2*y*bexpr/y**2*cexpr], [bexpr*cexpr]])

    assert derive_by_array(sexpr, [[x, y], [z, t]]) == Array([[bexpr/x*cexpr, 2*y*bexpr/y**2*cexpr], [bexpr*cexpr, bexpr/log(t)/t*cexpr]])
    assert derive_by_array(a, [[x, y], [z, t]]) == Array([[[bexpr/x*cexpr], [2*y*bexpr/y**2*cexpr]], [[bexpr*cexpr], [bexpr/log(t)/t*cexpr]]])
    assert derive_by_array([[x, y], [z, t]], [x, y]) == Array([[[1, 0], [0, 0]], [[0, 1], [0, 0]]])
    assert derive_by_array([[x, y], [z, t]], [[x, y], [z, t]]) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]],
                                                                         [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    assert diff(sexpr, t) == x*y**2*exp(z)*cos(x*y**2*exp(z)*log(t))/t
    assert diff(sexpr, Array([x, y, z])) == Array([bexpr/x*cexpr, 2*y*bexpr/y**2*cexpr, bexpr*cexpr])
    assert diff(a, Array([x, y, z])) == Array([[bexpr/x*cexpr], [2*y*bexpr/y**2*cexpr], [bexpr*cexpr]])

    assert diff(sexpr, Array([[x, y], [z, t]])) == Array([[bexpr/x*cexpr, 2*y*bexpr/y**2*cexpr], [bexpr*cexpr, bexpr/log(t)/t*cexpr]])
    assert diff(a, Array([[x, y], [z, t]])) == Array([[[bexpr/x*cexpr], [2*y*bexpr/y**2*cexpr]], [[bexpr*cexpr], [bexpr/log(t)/t*cexpr]]])
    assert diff(Array([[x, y], [z, t]]), Array([x, y])) == Array([[[1, 0], [0, 0]], [[0, 1], [0, 0]]])
    assert diff(Array([[x, y], [z, t]]), Array([[x, y], [z, t]])) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]],
                                                                         [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    # test for large scale sparse array
    for SparseArrayType in [ImmutableSparseNDimArray, MutableSparseNDimArray]:
        b = MutableSparseNDimArray({0:i, 1:j}, (10000, 20000))
        assert derive_by_array(b, i) == ImmutableSparseNDimArray({0: 1}, (10000, 20000))
        assert derive_by_array(b, (i, j)) == ImmutableSparseNDimArray({0: 1, 200000001: 1}, (2, 10000, 20000))

    #https://github.com/sympy/sympy/issues/20655
    U = Array([x, y, z])
    E = 2
    assert derive_by_array(E, U) ==  ImmutableDenseNDimArray([0, 0, 0])

