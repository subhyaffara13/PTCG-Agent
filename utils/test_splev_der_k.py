
def test_splev_der_k():
    # regression test for gh-2188: splev(x, tck, der=k) gives garbage or crashes
    # for x outside of knot range

    # test case from gh-2188
    tck = (np.array([0., 0., 2.5, 2.5]),
           np.array([-1.56679978, 2.43995873, 0., 0.]),
           1)
    t, c, k = tck
    x = np.array([-3, 0, 2.5, 3])

    # an explicit form of the linear spline
    xp_assert_close(splev(x, tck), c[0] + (c[1] - c[0]) * x/t[2])
    xp_assert_close(splev(x, tck, 1),
                    np.ones_like(x) * (c[1] - c[0]) / t[2]
    )

    # now check a random spline vs splder
    np.random.seed(1234)
    x = np.sort(np.random.random(30))
    y = np.random.random(30)
    t, c, k = splrep(x, y)

    x = [t[0] - 1., t[-1] + 1.]
    tck2 = splder((t, c, k), k)
    xp_assert_close(splev(x, (t, c, k), k), splev(x, tck2))

