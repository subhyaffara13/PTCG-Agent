
def test_broadcasting_in_moments_gh12192_regression():
    vals0 = stats.norm.moment(order=1, loc=np.array([1, 2, 3]), scale=[[1]])
    expected0 = np.array([[1., 2., 3.]])
    npt.assert_equal(vals0, expected0)
    assert vals0.shape == expected0.shape

    vals1 = stats.norm.moment(order=1, loc=np.array([[1], [2], [3]]),
                              scale=[1, 2, 3])
    expected1 = np.array([[1., 1., 1.], [2., 2., 2.], [3., 3., 3.]])
    npt.assert_equal(vals1, expected1)
    assert vals1.shape == expected1.shape

    vals2 = stats.chi.moment(order=1, df=[1., 2., 3.], loc=0., scale=1.)
    expected2 = np.array([0.79788456, 1.25331414, 1.59576912])
    npt.assert_allclose(vals2, expected2, rtol=1e-8)
    assert vals2.shape == expected2.shape

    vals3 = stats.chi.moment(order=1, df=[[1.], [2.], [3.]], loc=[0., 1., 2.],
                             scale=[-1., 0., 3.])
    expected3 = np.array([[np.nan, np.nan, 4.39365368],
                          [np.nan, np.nan, 5.75994241],
                          [np.nan, np.nan, 6.78730736]])
    npt.assert_allclose(vals3, expected3, rtol=1e-8)
    assert vals3.shape == expected3.shape

