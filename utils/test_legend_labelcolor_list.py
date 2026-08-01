
def test_legend_labelcolor_list():
    # test labelcolor for a list of colors
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10)*1, label='#1')
    ax.plot(np.arange(10), np.arange(10)*2, label='#2')
    ax.plot(np.arange(10), np.arange(10)*3, label='#3')

    leg = ax.legend(labelcolor=['r', 'g', 'b'])
    for text, color in zip(leg.get_texts(), ['r', 'g', 'b']):
        assert mpl.colors.same_color(text.get_color(), color)

