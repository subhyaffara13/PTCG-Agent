
def test_legend_pathcollection_labelcolor_markerfacecolor_iterable():
    # test the labelcolor for labelcolor='markerfacecolor' on PathCollection
    # with iterable colors
    fig, ax = plt.subplots()
    colors = np.array(['r', 'g', 'b', 'c', 'm'] * 2)
    ax.scatter(np.arange(10), np.arange(10), label='#1', facecolor=colors)

    leg = ax.legend(labelcolor='markerfacecolor')
    for text, color in zip(leg.get_texts(), ['k']):
        assert mpl.colors.same_color(text.get_color(), color)

