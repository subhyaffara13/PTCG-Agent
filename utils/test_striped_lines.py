
def test_striped_lines(fig_test, fig_ref, gapcolor):
    ax_test = fig_test.add_subplot(111)
    ax_ref = fig_ref.add_subplot(111)

    for ax in [ax_test, ax_ref]:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 1)

    x = range(1, 6)
    linestyles = [':', '-', '--']

    ax_test.vlines(x, 0, 1, linewidth=20, linestyle=linestyles, gapcolor=gapcolor,
                   alpha=0.5)

    if isinstance(gapcolor, str):
        gapcolor = [gapcolor]

    for x, gcol, ls in zip(x, itertools.cycle(gapcolor),
                           itertools.cycle(linestyles)):
        ax_ref.axvline(x, 0, 1, linewidth=20, linestyle=ls, gapcolor=gcol, alpha=0.5)


def test_striped_lines(text_placeholders):
    rng = np.random.default_rng(19680801)
    _, ax = plt.subplots()
    ax.plot(rng.uniform(size=12), color='orange', gapcolor='blue',
            linestyle='--', lw=5, label='blue in orange')
    ax.plot(rng.uniform(size=12), color='red', gapcolor='black',
            linestyle=(0, (2, 5, 4, 2)), lw=5, label='black in red', alpha=0.5)
    ax.legend(handlelength=5)

