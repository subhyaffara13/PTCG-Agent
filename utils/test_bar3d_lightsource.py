
def test_bar3d_lightsource():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection="3d")

    ls = mcolors.LightSource(azdeg=0, altdeg=90)

    length, width = 3, 4
    area = length * width

    x, y = np.meshgrid(np.arange(length), np.arange(width))
    x = x.ravel()
    y = y.ravel()
    dz = x + y

    color = [cm.coolwarm(i/area) for i in range(area)]

    collection = ax.bar3d(x=x, y=y, z=0,
                          dx=1, dy=1, dz=dz,
                          color=color, shade=True, lightsource=ls)

    # Testing that the custom 90° lightsource produces different shading on
    # the top facecolors compared to the default, and that those colors are
    # precisely (within floating point rounding errors of 4 ULP) the colors
    # from the colormap, due to the illumination parallel to the z-axis.
    np.testing.assert_array_max_ulp(color, collection._facecolor3d[1::6], 4)

