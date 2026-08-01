
def test_legend_pathcollection_labelcolor_linecolor_iterable():
    # test the labelcolor for labelcolor='linecolor' on PathCollection
    # with iterable colors
    fig, ax = plt.subplots()
    colors = np.array(['r', 'g', 'b', 'c', 'm'] * 2)
    ax.scatter(np.arange(10), np.arange(10), label='#1', c=colors)

    leg = ax.legend(labelcolor='linecolor')
    text, = leg.get_texts()
    assert mpl.colors.same_color(text.get_color(), 'black')

