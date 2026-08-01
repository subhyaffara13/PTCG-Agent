
def test_kappa4_array_gh13582():
    h = np.array([-0.5, 2.5, 3.5, 4.5, -3])
    k = np.array([-0.5, 1, -1.5, 0, 3.5])
    moments = 'mvsk'
    res = np.array([[stats.kappa4.stats(h[i], k[i], moments=moment)
                   for i in range(5)] for moment in moments])
    res2 = np.array(stats.kappa4.stats(h, k, moments=moments))
    npt.assert_allclose(res, res2)

    # https://github.com/scipy/scipy/pull/15250#discussion_r775112913
    h = np.array([-1, -1/4, -1/4, 1, -1, 0])
    k = np.array([1, 1, 1/2, -1/3, -1, 0])
    res = np.array([[stats.kappa4.stats(h[i], k[i], moments=moment)
                   for i in range(6)] for moment in moments])
    res2 = np.array(stats.kappa4.stats(h, k, moments=moments))
    npt.assert_allclose(res, res2)

    # https://github.com/scipy/scipy/pull/15250#discussion_r775115021
    h = np.array([-1, -0.5, 1])
    k = np.array([-1, -0.5, 0, 1])[:, None]
    res2 = np.array(stats.kappa4.stats(h, k, moments=moments))
    assert res2.shape == (4, 4, 3)

