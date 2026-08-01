
def test_legend_pathcollection_labelcolor_markerfacecolor():
    # test the labelcolor for labelcolor='markerfacecolor' on PathCollection
    fig, ax = plt.subplots()
    ax.scatter(np.arange(10), np.arange(10)*1, label='#1', facecolor='r')
    ax.scatter(np.arange(10), np.arange(10)*2, label='#2', facecolor='g')
    ax.scatter(np.arange(10), np.arange(10)*3, label='#3', facecolor='b')

    leg = ax.legend(labelcolor='markerfacecolor')
    for text, color in zip(leg.get_texts(), ['r', 'g', 'b']):
        assert mpl.colors.same_color(text.get_color(), color)

