
def test_multivar_alpha_mixing():
    # test creation of a custom colormap using 'rainbow'
    # and a colormap that goes from alpha = 1 to alpha = 0
    rainbow = mpl.colormaps['rainbow']
    alpha = np.zeros((256, 4))
    alpha[:, 3] = np.linspace(1, 0, 256)
    alpha_cmap = mpl.colors.LinearSegmentedColormap.from_list('from_list', alpha)

    cmap = mpl.colors.MultivarColormap((rainbow, alpha_cmap), 'sRGB_add')
    y, x = np.mgrid[0:10, 0:10]/9
    im = cmap((y, x))

    fig, ax = plt.subplots()
    ax.imshow(im, interpolation='nearest')
    remove_ticks_and_titles(fig)

