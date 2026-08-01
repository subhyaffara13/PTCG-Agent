
def test_bivariate_cmap_shapes():
    x_0 = np.repeat(np.linspace(-0.1, 1.1, 10, dtype='float32')[None, :], 10, axis=0)
    x_1 = x_0.T

    fig, axes = plt.subplots(1, 4, figsize=(10, 2))

    # shape = 'square'
    cmap = mpl.bivar_colormaps['BiPeak']
    axes[0].imshow(cmap((x_0, x_1)), interpolation='nearest')

    # shape = 'circle'
    cmap = mpl.bivar_colormaps['BiCone']
    axes[1].imshow(cmap((x_0, x_1)), interpolation='nearest')

    # shape = 'ignore'
    cmap = mpl.bivar_colormaps['BiPeak']
    cmap = cmap.with_extremes(shape='ignore')
    axes[2].imshow(cmap((x_0, x_1)), interpolation='nearest')

    # shape = circleignore
    cmap = mpl.bivar_colormaps['BiCone']
    cmap = cmap.with_extremes(shape='circleignore')
    axes[3].imshow(cmap((x_0, x_1)), interpolation='nearest')
    remove_ticks_and_titles(fig)

