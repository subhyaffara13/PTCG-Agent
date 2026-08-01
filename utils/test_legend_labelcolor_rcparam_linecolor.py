
def test_legend_labelcolor_rcparam_linecolor():
    # test the rcParams legend.labelcolor for a linecolor
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10)*1, label='#1', color='r')
    ax.plot(np.arange(10), np.arange(10)*2, label='#2', color='g')
    ax.plot(np.arange(10), np.arange(10)*3, label='#3', color='b')

    mpl.rcParams['legend.labelcolor'] = 'linecolor'
    leg = ax.legend()
    for text, color in zip(leg.get_texts(), ['r', 'g', 'b']):
        assert mpl.colors.same_color(text.get_color(), color)

