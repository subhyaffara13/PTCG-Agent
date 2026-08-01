
def test_set_get_ticklabels():
    # test issue 2246
    fig, ax = plt.subplots(2)
    ha = ['normal', 'set_x/yticklabels']

    ax[0].plot(np.arange(10))
    ax[0].set_title(ha[0])

    ax[1].plot(np.arange(10))
    ax[1].set_title(ha[1])

    # set ticklabel to 1 plot in normal way
    ax[0].set_xticks(range(10))
    ax[0].set_yticks(range(10))
    ax[0].set_xticklabels(['a', 'b', 'c', 'd'] + 6 * [''])
    ax[0].set_yticklabels(['11', '12', '13', '14'] + 6 * [''])

    # set ticklabel to the other plot, expect the 2 plots have same label
    # setting pass get_ticklabels return value as ticklabels argument
    ax[1].set_xticks(ax[0].get_xticks())
    ax[1].set_yticks(ax[0].get_yticks())
    ax[1].set_xticklabels(ax[0].get_xticklabels())
    ax[1].set_yticklabels(ax[0].get_yticklabels())

