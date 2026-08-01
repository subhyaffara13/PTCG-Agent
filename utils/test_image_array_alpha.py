
def test_image_array_alpha(fig_test, fig_ref):
    """Per-pixel alpha channel test."""
    x = np.linspace(0, 1)
    xx, yy = np.meshgrid(x, x)

    zz = np.exp(- 3 * ((xx - 0.5) ** 2) + (yy - 0.7 ** 2))
    alpha = zz / zz.max()

    cmap = mpl.colormaps['viridis']
    ax = fig_test.add_subplot()
    ax.imshow(zz, alpha=alpha, cmap=cmap, interpolation='nearest')

    ax = fig_ref.add_subplot()
    rgba = cmap(colors.Normalize()(zz))
    rgba[..., -1] = alpha
    ax.imshow(rgba, interpolation='nearest')

