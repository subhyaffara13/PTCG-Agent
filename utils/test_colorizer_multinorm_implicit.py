
def test_colorizer_multinorm_implicit():
    ca = mcolorizer.Colorizer('BiOrangeBlue')
    ca.vmin = (0, 0)
    ca.vmax = (1, 1)

    # test call with two single values
    data = [0.1, 0.2]
    res = (0.098039, 0.149020, 0.2, 1.0)
    assert_array_almost_equal(ca.to_rgba(data), res)

    # test call with two 1d arrays
    data = [[0.1, 0.2], [0.3, 0.4]]
    res = [[0.09803922, 0.19803922, 0.29803922, 1.],
           [0.2, 0.3, 0.4, 1.]]
    assert_array_almost_equal(ca.to_rgba(data), res)

    # test call with two 2d arrays
    data = [np.linspace(0, 1, 12).reshape(3, 4),
            np.linspace(1, 0, 12).reshape(3, 4)]
    res = np.array([[[0., 0.5, 1., 1.],
                     [0.09019608, 0.5, 0.90980392, 1.],
                     [0.18039216, 0.5, 0.81960784, 1.],
                     [0.27058824, 0.5, 0.72941176, 1.]],
                    [[0.36470588, 0.5, 0.63529412, 1.],
                     [0.45490196, 0.5, 0.54509804, 1.],
                     [0.54509804, 0.5, 0.45490196, 1.],
                     [0.63529412, 0.5, 0.36470588, 1.]],
                    [[0.72941176, 0.5, 0.27058824, 1.],
                     [0.81960784, 0.5, 0.18039216, 1.],
                     [0.90980392, 0.5, 0.09019608, 1.],
                     [1., 0.5, 0., 1.]]])
    assert_array_almost_equal(ca.to_rgba(data), res)

    with pytest.raises(ValueError, match=("This MultiNorm has 2 components, "
                                          "but got a sequence with 3 elements")):
        ca.to_rgba([0.1, 0.2, 0.3])
    with pytest.raises(ValueError, match=("This MultiNorm has 2 components, "
                                          "but got a sequence with 1 elements")):
        ca.to_rgba([[0.1]])

    # test multivariate
    ca = mcolorizer.Colorizer('3VarAddA')
    ca.vmin = (-0.1, -0.2, -0.3)
    ca.vmax = (0.1, 0.2, 0.3)

    data = [0.1, 0.1, 0.1]
    res = (0.712612, 0.896847, 0.954494, 1.0)
    assert_array_almost_equal(ca.to_rgba(data), res)

