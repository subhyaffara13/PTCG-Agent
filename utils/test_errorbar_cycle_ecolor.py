
def test_errorbar_cycle_ecolor(fig_test, fig_ref):
    x = np.arange(0.1, 4, 0.5)
    y = [np.exp(-x+n) for n in range(4)]

    axt = fig_test.subplots()
    axr = fig_ref.subplots()

    for yi, color in zip(y, ['C0', 'C1', 'C2', 'C3']):
        axt.errorbar(x, yi, yerr=(yi * 0.25), linestyle='-',
                     marker='o', ecolor='black')
        axr.errorbar(x, yi, yerr=(yi * 0.25), linestyle='-',
                     marker='o', color=color, ecolor='black')

