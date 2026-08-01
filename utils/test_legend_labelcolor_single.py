
def test_legend_labelcolor_single(color):
    # test labelcolor for a single color
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10)*1, label='#1')
    ax.plot(np.arange(10), np.arange(10)*2, label='#2')
    ax.plot(np.arange(10), np.arange(10)*3, label='#3')

    leg = ax.legend(labelcolor=color)
    for text in leg.get_texts():
        assert mpl.colors.same_color(text.get_color(), color)

