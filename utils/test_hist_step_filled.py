
def test_hist_step_filled():
    np.random.seed(0)
    x = np.random.randn(1000, 3)
    n_bins = 10

    kwargs = [{'fill': True}, {'fill': False}, {'fill': None}, {}]*2
    types = ['step']*4+['stepfilled']*4
    fig, axs = plt.subplots(nrows=2, ncols=4)

    for kg, _type, ax in zip(kwargs, types, axs.flat):
        ax.hist(x, n_bins, histtype=_type, stacked=True, **kg)
        ax.set_title(f'{kg}/{_type}')
        ax.set_ylim(bottom=-50)

    patches = axs[0, 0].patches
    assert all(p.get_facecolor() == p.get_edgecolor() for p in patches)

