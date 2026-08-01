
def test_legend_pathcollection_labelcolor_linecolor_cmap():
    # test the labelcolor for labelcolor='linecolor' on PathCollection
    # with a colormap
    fig, ax = plt.subplots()
    ax.scatter(np.arange(10), np.arange(10), c=np.arange(10), label='#1')

    leg = ax.legend(labelcolor='linecolor')
    text, = leg.get_texts()
    assert mpl.colors.same_color(text.get_color(), 'black')

