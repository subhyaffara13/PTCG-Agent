
def test_lw_scaling():
    th = np.linspace(0, 32)
    fig, ax = plt.subplots()
    lins_styles = ['dashed', 'dotted', 'dashdot']
    cy = cycler(matplotlib.rcParams['axes.prop_cycle'])
    for j, (ls, sty) in enumerate(zip(lins_styles, cy)):
        for lw in np.linspace(.5, 10, 10):
            ax.plot(th, j*np.ones(50) + .1 * lw, linestyle=ls, lw=lw, **sty)

