
def test_legend_pathcollection_labelcolor_markfacecolor_cmap():
    # test the labelcolor for labelcolor='markerfacecolor' on PathCollection
    # with colormaps
    fig, ax = plt.subplots()
    colors = mpl.colormaps["viridis"](np.random.rand(10))
    ax.scatter(
        np.arange(10),
        np.arange(10),
        label='#1',
        c=colors
    )

    leg = ax.legend(labelcolor='markerfacecolor')
    for text, color in zip(leg.get_texts(), ['k']):
        assert mpl.colors.same_color(text.get_color(), color)

