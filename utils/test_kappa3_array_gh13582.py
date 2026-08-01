
def test_kappa3_array_gh13582():
    # https://github.com/scipy/scipy/pull/15140#issuecomment-994958241
    shapes = [0.5, 1.5, 2.5, 3.5, 4.5]
    moments = 'mvsk'
    res = np.array([[stats.kappa3.stats(shape, moments=moment)
                   for shape in shapes] for moment in moments])
    res2 = np.array(stats.kappa3.stats(shapes, moments=moments))
    npt.assert_allclose(res, res2)

