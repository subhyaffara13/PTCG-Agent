
def test_legend_labelcolor_rcparam_single(color):
    # test the rcParams legend.labelcolor for a single color
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10)*1, label='#1')
    ax.plot(np.arange(10), np.arange(10)*2, label='#2')
    ax.plot(np.arange(10), np.arange(10)*3, label='#3')

    mpl.rcParams['legend.labelcolor'] = color
    leg = ax.legend()
    for text in leg.get_texts():
        assert mpl.colors.same_color(text.get_color(), color)

