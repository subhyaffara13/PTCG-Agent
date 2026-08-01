
def test_minorticks_toggle():
    """
    Test toggling minor ticks

    Test `.Axis.minorticks_on()` and `.Axis.minorticks_off()`. Testing is
    limited to a subset of built-in scales - `'linear'`, `'log'`, `'asinh'`
    and `'logit'`. `symlog` scale does not seem to have a working minor
    locator and is omitted. In future, this test should cover all scales in
    `matplotlib.scale.get_scale_names()`.
    """
    fig = plt.figure()
    def minortickstoggle(xminor, yminor, scale, i):
        ax = fig.add_subplot(2, 2, i)
        ax.set_xscale(scale)
        ax.set_yscale(scale)
        if not xminor and not yminor:
            ax.minorticks_off()
        if xminor and not yminor:
            ax.xaxis.minorticks_on()
            ax.yaxis.minorticks_off()
        if not xminor and yminor:
            ax.xaxis.minorticks_off()
            ax.yaxis.minorticks_on()
        if xminor and yminor:
            ax.minorticks_on()

        assert (len(ax.xaxis.get_minor_ticks()) > 0) == xminor
        assert (len(ax.yaxis.get_minor_ticks()) > 0) == yminor

    scales = ['linear', 'log', 'asinh', 'logit']
    for scale in scales:
        minortickstoggle(False, False, scale, 1)
        minortickstoggle(True, False, scale, 2)
        minortickstoggle(False, True, scale, 3)
        minortickstoggle(True, True, scale, 4)
        fig.clear()

    plt.close(fig)

