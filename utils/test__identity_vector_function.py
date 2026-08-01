
def test_IdentityVectorFunction():
    x0 = np.zeros(3)

    f1 = IdentityVectorFunction(x0, None)
    f2 = IdentityVectorFunction(x0, False)
    f3 = IdentityVectorFunction(x0, True)

    assert_(f1.sparse_jacobian)
    assert_(not f2.sparse_jacobian)
    assert_(f3.sparse_jacobian)

    x = np.array([-1, 2, 1])
    v = np.array([-2, 3, 0])

    assert_array_equal(f1.fun(x), x)
    assert_array_equal(f2.fun(x), x)

    assert_array_equal(f1.jac(x).toarray(), np.eye(3))
    assert_array_equal(f2.jac(x), np.eye(3))

    assert_array_equal(f1.hess(x, v).toarray(), np.zeros((3, 3)))

