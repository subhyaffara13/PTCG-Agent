
def test_legend_pathcollection_labelcolor_linecolor():
    # test the labelcolor for labelcolor='linecolor' on PathCollection
    fig, ax = plt.subplots()
    ax.scatter(np.arange(10), np.arange(10)*1, label='#1', c='r')
    ax.scatter(np.arange(10), np.arange(10)*2, label='#2', c='g')
    ax.scatter(np.arange(10), np.arange(10)*3, label='#3', c='b')

    leg = ax.legend(labelcolor='linecolor')
    for text, color in zip(leg.get_texts(), ['r', 'g', 'b']):
        assert mpl.colors.same_color(text.get_color(), color)

