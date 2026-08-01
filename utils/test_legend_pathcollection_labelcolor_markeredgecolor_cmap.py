
def test_legend_pathcollection_labelcolor_markeredgecolor_cmap():
    # test the labelcolor for labelcolor='markeredgecolor' on PathCollection
    # with a colormap
    fig, ax = plt.subplots()
    edgecolors = mpl.colormaps["viridis"](np.random.rand(10))
    ax.scatter(
        np.arange(10),
        np.arange(10),
        label='#1',
        c=np.arange(10),
        edgecolor=edgecolors,
        cmap="Reds"
    )

    leg = ax.legend(labelcolor='markeredgecolor')
    for text, color in zip(leg.get_texts(), ['k']):
        assert mpl.colors.same_color(text.get_color(), color)

