
def test_geequ():
    desired_real = np.array([[0.6250, 1.0000, 0.0393, -0.4269],
                             [1.0000, -0.5619, -1.0000, -1.0000],
                             [0.5874, -1.0000, -0.0596, -0.5341],
                             [-1.0000, -0.5946, -0.0294, 0.9957]])

    desired_cplx = np.array([[-0.2816+0.5359*1j,
                              0.0812+0.9188*1j,
                              -0.7439-0.2561*1j],
                             [-0.3562-0.2954*1j,
                              0.9566-0.0434*1j,
                              -0.0174+0.1555*1j],
                             [0.8607+0.1393*1j,
                              -0.2759+0.7241*1j,
                              -0.1642-0.1365*1j]])

    for ind, dtype in enumerate(DTYPES):
        if ind < 2:
            # Use examples from the NAG documentation
            A = np.array([[1.80e+10, 2.88e+10, 2.05e+00, -8.90e+09],
                          [5.25e+00, -2.95e+00, -9.50e-09, -3.80e+00],
                          [1.58e+00, -2.69e+00, -2.90e-10, -1.04e+00],
                          [-1.11e+00, -6.60e-01, -5.90e-11, 8.00e-01]])
            A = A.astype(dtype)
        else:
            A = np.array([[-1.34e+00, 0.28e+10, -6.39e+00],
                          [-1.70e+00, 3.31e+10, -0.15e+00],
                          [2.41e-10, -0.56e+00, -0.83e-10]], dtype=dtype)
            A += np.array([[2.55e+00, 3.17e+10, -2.20e+00],
                           [-1.41e+00, -0.15e+10, 1.34e+00],
                           [0.39e-10, 1.47e+00, -0.69e-10]])*1j

            A = A.astype(dtype)

        geequ = get_lapack_funcs('geequ', dtype=dtype)
        r, c, rowcnd, colcnd, amax, info = geequ(A)

        if ind < 2:
            assert_allclose(desired_real.astype(dtype), r[:, None]*A*c,
                            rtol=0, atol=1e-4)
        else:
            assert_allclose(desired_cplx.astype(dtype), r[:, None]*A*c,
                            rtol=0, atol=1e-4)

