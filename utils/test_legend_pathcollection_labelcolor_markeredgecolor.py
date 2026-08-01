
def test_legend_pathcollection_labelcolor_markeredgecolor():
    # test the labelcolor for labelcolor='markeredgecolor' on PathCollection
    fig, ax = plt.subplots()
    ax.scatter(np.arange(10), np.arange(10)*1, label='#1', edgecolor='r')
    ax.scatter(np.arange(10), np.arange(10)*2, label='#2', edgecolor='g')
    ax.scatter(np.arange(10), np.arange(10)*3, label='#3', edgecolor='b')

    leg = ax.legend(labelcolor='markeredgecolor')
    for text, color in zip(leg.get_texts(), ['r', 'g', 'b']):
        assert mpl.colors.same_color(text.get_color(), color)

