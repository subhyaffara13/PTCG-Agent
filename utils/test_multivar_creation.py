
def test_multivar_creation():
    # test creation of a custom multivariate colorbar
    blues = mpl.colormaps['Blues']
    cmap = mpl.colors.MultivarColormap((blues, 'Oranges'), 'sRGB_sub')
    y, x = np.mgrid[0:3, 0:3]/2
    im = cmap((y, x))
    res = np.array([[[0.96862745, 0.94509804, 0.92156863, 1],
                     [0.96004614, 0.53504037, 0.23277201, 1],
                     [0.46666667, 0.1372549, 0.01568627, 1]],
                    [[0.41708574, 0.64141484, 0.75980008, 1],
                     [0.40850442, 0.23135717, 0.07100346, 1],
                     [0, 0, 0, 1]],
                    [[0.03137255, 0.14901961, 0.34117647, 1],
                     [0.02279123, 0, 0, 1],
                     [0, 0, 0, 1]]])
    assert_allclose(im,  res, atol=0.01)

    with pytest.raises(ValueError, match="colormaps must be a list of"):
        cmap = mpl.colors.MultivarColormap((blues, [blues]), 'sRGB_sub')
    with pytest.raises(ValueError, match="A MultivarColormap must"):
        cmap = mpl.colors.MultivarColormap('blues', 'sRGB_sub')
    with pytest.raises(ValueError, match="A MultivarColormap must"):
        cmap = mpl.colors.MultivarColormap((blues), 'sRGB_sub')

