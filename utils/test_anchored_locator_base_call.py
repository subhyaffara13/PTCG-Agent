
def test_anchored_locator_base_call():
    fig = plt.figure(figsize=(3, 3))
    fig1, fig2 = fig.subfigures(nrows=2, ncols=1)

    ax = fig1.subplots()
    ax.set(aspect=1, xlim=(-15, 15), ylim=(-20, 5))
    ax.set(xticks=[], yticks=[])

    Z = cbook.get_sample_data("axes_grid/bivariate_normal.npy")
    extent = (-3, 4, -4, 3)

    axins = zoomed_inset_axes(ax, zoom=2, loc="upper left")
    axins.set(xticks=[], yticks=[])

    axins.imshow(Z, extent=extent, origin="lower")

