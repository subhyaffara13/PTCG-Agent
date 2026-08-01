
def test_spalde_nc():
    # regression test for https://github.com/scipy/scipy/issues/19002
    # here len(t) = 29 and len(c) = 25 (== len(t) - k - 1)
    x = np.asarray([-10., -9., -8., -7., -6., -5., -4., -3., -2.5, -2., -1.5,
                    -1., -0.5, 0., 0.5, 1., 1.5, 2., 2.5, 3., 4., 5., 6.],
                    dtype="float")
    t = [-10.0, -10.0, -10.0, -10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0,
         -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0,
         5.0, 6.0, 6.0, 6.0, 6.0]
    c = np.asarray([1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                    0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    k = 3

    res = spalde(x, (t, c, k))
    res = np.vstack(res)
    res_splev = np.asarray([splev(x, (t, c, k), nu) for nu in range(4)])
    xp_assert_close(res, res_splev.T, atol=1e-15)

