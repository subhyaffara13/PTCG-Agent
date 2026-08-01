
def test_errorbar_every(fig_test, fig_ref):
    x = np.linspace(0, 1, 15)
    y = x * (1-x)
    yerr = y/6

    ax_ref = fig_ref.subplots()
    ax_test = fig_test.subplots()

    for color, shift in zip('rgbk', [0, 0, 2, 7]):
        y += .02

        # Check errorevery using an explicit offset and step.
        ax_test.errorbar(x, y, yerr, errorevery=(shift, 4),
                         capsize=4, c=color)

        # Using manual errorbars
        # n.b. errorbar draws the main plot at z=2.1 by default
        ax_ref.plot(x, y, c=color, zorder=2.1)
        ax_ref.errorbar(x[shift::4], y[shift::4], yerr[shift::4],
                        capsize=4, c=color, fmt='none')

    # Check that markevery is propagated to line, without affecting errorbars.
    ax_test.errorbar(x, y + 0.1, yerr, markevery=(1, 4), capsize=4, fmt='o')
    ax_ref.plot(x[1::4], y[1::4] + 0.1, 'o', zorder=2.1)
    ax_ref.errorbar(x, y + 0.1, yerr, capsize=4, fmt='none')

    # Check that passing a slice to markevery/errorevery works.
    ax_test.errorbar(x, y + 0.2, yerr, errorevery=slice(2, None, 3),
                     markevery=slice(2, None, 3),
                     capsize=4, c='C0', fmt='o')
    ax_ref.plot(x[2::3], y[2::3] + 0.2, 'o', c='C0', zorder=2.1)
    ax_ref.errorbar(x[2::3], y[2::3] + 0.2, yerr[2::3],
                    capsize=4, c='C0', fmt='none')

    # Check that passing an iterable to markevery/errorevery works.
    ax_test.errorbar(x, y + 0.2, yerr, errorevery=[False, True, False] * 5,
                     markevery=[False, True, False] * 5,
                     capsize=4, c='C1', fmt='o')
    ax_ref.plot(x[1::3], y[1::3] + 0.2, 'o', c='C1', zorder=2.1)
    ax_ref.errorbar(x[1::3], y[1::3] + 0.2, yerr[1::3],
                    capsize=4, c='C1', fmt='none')

