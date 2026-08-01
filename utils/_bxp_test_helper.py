
def _bxp_test_helper(
        stats_kwargs={}, transform_stats=lambda s: s, bxp_kwargs={}):
    np.random.seed(937)
    logstats = mpl.cbook.boxplot_stats(
        np.random.lognormal(mean=1.25, sigma=1., size=(37, 4)), **stats_kwargs)
    fig, ax = plt.subplots()
    if bxp_kwargs.get('orientation', 'vertical') == 'vertical':
        ax.set_yscale('log')
    else:
        ax.set_xscale('log')
    # Work around baseline images generate back when bxp did not respect the
    # boxplot.boxprops.linewidth rcParam when patch_artist is False.
    if not bxp_kwargs.get('patch_artist', False):
        mpl.rcParams['boxplot.boxprops.linewidth'] = \
            mpl.rcParams['lines.linewidth']
    ax.bxp(transform_stats(logstats), **bxp_kwargs)

