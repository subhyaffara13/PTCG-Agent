
def test_subfigure():
    np.random.seed(19680801)
    fig = plt.figure(layout='constrained')
    sub = fig.subfigures(1, 2)

    axs = sub[0].subplots(2, 2)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[0].colorbar(pc, ax=axs)
    sub[0].suptitle('Left Side')
    sub[0].set_facecolor('white')

    axs = sub[1].subplots(1, 3)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[1].colorbar(pc, ax=axs, location='bottom')
    sub[1].suptitle('Right Side')
    sub[1].set_facecolor('white')

    fig.suptitle('Figure suptitle', fontsize='xx-large')

    # below tests for the draw zorder of subfigures.
    leg = fig.legend(handles=[plt.Line2D([0], [0], label='Line{}'.format(i))
                     for i in range(5)], loc='center')
    sub[0].set_zorder(leg.get_zorder() - 1)
    sub[1].set_zorder(leg.get_zorder() + 1)

