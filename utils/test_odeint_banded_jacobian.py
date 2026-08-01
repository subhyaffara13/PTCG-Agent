
def test_odeint_banded_jacobian():
    # Test the use of the `Dfun`, `ml` and `mu` options of odeint.

    def func(y, t, c):
        return c.dot(y)

    def jac(y, t, c):
        return c

    def jac_transpose(y, t, c):
        return c.T.copy(order='C')

    def bjac_rows(y, t, c):
        jac = np.vstack((np.r_[0, np.diag(c, 1)],
                            np.diag(c),
                            np.r_[np.diag(c, -1), 0],
                            np.r_[np.diag(c, -2), 0, 0]))
        return jac

    def bjac_cols(y, t, c):
        return bjac_rows(y, t, c).T.copy(order='C')

    c = array([[-205, 0.01, 0.00, 0.0],
               [0.1, -2.50, 0.02, 0.0],
               [1e-3, 0.01, -2.0, 0.01],
               [0.00, 0.00, 0.1, -1.0]])

    y0 = np.ones(4)
    t = np.array([0, 5, 10, 100])

    # Use the full Jacobian.
    sol1, info1 = odeint(func, y0, t, args=(c,), full_output=True,
                         atol=1e-13, rtol=1e-11, mxstep=10000,
                         Dfun=jac)

    # Use the transposed full Jacobian, with col_deriv=True.
    sol2, info2 = odeint(func, y0, t, args=(c,), full_output=True,
                         atol=1e-13, rtol=1e-11, mxstep=10000,
                         Dfun=jac_transpose, col_deriv=True)

    # Use the banded Jacobian.
    sol3, info3 = odeint(func, y0, t, args=(c,), full_output=True,
                         atol=1e-13, rtol=1e-11, mxstep=10000,
                         Dfun=bjac_rows, ml=2, mu=1)

    # Use the transposed banded Jacobian, with col_deriv=True.
    sol4, info4 = odeint(func, y0, t, args=(c,), full_output=True,
                         atol=1e-13, rtol=1e-11, mxstep=10000,
                         Dfun=bjac_cols, ml=2, mu=1, col_deriv=True)

    assert_allclose(sol1, sol2, err_msg="sol1 != sol2")
    assert_allclose(sol1, sol3, atol=1e-12, err_msg="sol1 != sol3")
    assert_allclose(sol3, sol4, err_msg="sol3 != sol4")

    # Verify that the number of jacobian evaluations was the same for the
    # calls of odeint with a full jacobian and with a banded jacobian. This is
    # a regression test--there was a bug in the handling of banded jacobians
    # that resulted in an incorrect jacobian matrix being passed to the LSODA
    # code.  That would cause errors or excessive jacobian evaluations.
    assert_array_equal(info1['nje'], info2['nje'])
    assert_array_equal(info3['nje'], info4['nje'])

    # Test the use of tfirst
    sol1ty, info1ty = odeint(lambda t, y, c: func(y, t, c), y0, t, args=(c,),
                             full_output=True, atol=1e-13, rtol=1e-11,
                             mxstep=10000,
                             Dfun=lambda t, y, c: jac(y, t, c), tfirst=True)
    # The code should execute the exact same sequence of floating point
    # calculations, so these should be exactly equal. We'll be safe and use
    # a small tolerance.
    assert_allclose(sol1, sol1ty, rtol=1e-12, err_msg="sol1 != sol1ty")

