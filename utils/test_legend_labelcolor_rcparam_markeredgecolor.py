
def test_legend_labelcolor_rcparam_markeredgecolor():
    # test the labelcolor for labelcolor='markeredgecolor'
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10)*1, label='#1', markeredgecolor='r')
    ax.plot(np.arange(10), np.arange(10)*2, label='#2', markeredgecolor='g')
    ax.plot(np.arange(10), np.arange(10)*3, label='#3', markeredgecolor='b')

    mpl.rcParams['legend.labelcolor'] = 'markeredgecolor'
    leg = ax.legend()
    for text, color in zip(leg.get_texts(), ['r', 'g', 'b']):
        assert mpl.colors.same_color(text.get_color(), color)

