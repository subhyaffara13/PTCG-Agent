
def test_light_source_shading_empty_mask():
    y, x = np.mgrid[-1.2:1.2:8j, -1.2:1.2:8j]
    z0 = 10 * np.cos(x**2 + y**2)
    z1 = np.ma.array(z0)

    cmap = plt.colormaps["copper"]
    ls = mcolors.LightSource(315, 45)
    rgb0 = ls.shade(z0, cmap)
    rgb1 = ls.shade(z1, cmap)

    assert_array_almost_equal(rgb0, rgb1)

