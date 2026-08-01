
def test_mixed_errorbar_polar_caps():
    """
    Mix several polar errorbar use cases in a single test figure.

    It is advisable to position individual points off the grid. If there are
    problems with reproducibility of this test, consider removing grid.
    """
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')

    # symmetric errorbars
    th_sym = [1, 2, 3]
    r_sym = [0.9]*3
    ax.errorbar(th_sym, r_sym, xerr=0.35, yerr=0.2, fmt="o")

    # long errorbars
    th_long = [np.pi/2 + .1, np.pi + .1]
    r_long = [1.8, 2.2]
    ax.errorbar(th_long, r_long, xerr=0.8 * np.pi, yerr=0.15, fmt="o")

    # asymmetric errorbars
    th_asym = [4*np.pi/3 + .1, 5*np.pi/3 + .1, 2*np.pi-0.1]
    r_asym = [1.1]*3
    xerr = [[.3, .3, .2], [.2, .3, .3]]
    yerr = [[.35, .5, .5], [.5, .35, .5]]
    ax.errorbar(th_asym, r_asym, xerr=xerr, yerr=yerr, fmt="o")

    # overlapping errorbar
    th_over = [2.1]
    r_over = [3.1]
    ax.errorbar(th_over, r_over, xerr=10, yerr=.2, fmt="o")

