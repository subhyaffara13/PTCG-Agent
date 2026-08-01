
def test_errorbar_with_prop_cycle(fig_test, fig_ref):
    ax = fig_ref.subplots()
    ax.errorbar(x=[2, 4, 10], y=[0, 1, 2], yerr=0.5,
                ls='--', marker='s', mfc='k')
    ax.errorbar(x=[2, 4, 10], y=[2, 3, 4], yerr=0.5, color='tab:green',
                ls=':', marker='s', mfc='y')
    ax.errorbar(x=[2, 4, 10], y=[4, 5, 6], yerr=0.5, fmt='tab:blue',
                ls='-.', marker='o', mfc='c')
    ax.set_xlim(1, 11)

    _cycle = cycler(ls=['--', ':', '-.'], marker=['s', 's', 'o'],
                    mfc=['k', 'y', 'c'], color=['b', 'g', 'r'])
    plt.rc("axes", prop_cycle=_cycle)
    ax = fig_test.subplots()
    ax.errorbar(x=[2, 4, 10], y=[0, 1, 2], yerr=0.5)
    ax.errorbar(x=[2, 4, 10], y=[2, 3, 4], yerr=0.5, color='tab:green')
    ax.errorbar(x=[2, 4, 10], y=[4, 5, 6], yerr=0.5, fmt='tab:blue')
    ax.set_xlim(1, 11)

