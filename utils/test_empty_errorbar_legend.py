
def test_empty_errorbar_legend():
    fig, ax = plt.subplots()
    ax.errorbar([], [], xerr=[], label='empty y')
    ax.errorbar([], [], yerr=[], label='empty x')
    ax.legend()

