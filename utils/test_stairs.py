
def test_stairs(fig_test, fig_ref):
    import matplotlib.lines as mlines
    y = np.array([6, 14, 32, 37, 48, 32, 21,  4])  # hist
    x = np.array([1., 2., 3., 4., 5., 6., 7., 8., 9.])  # bins

    test_axes = fig_test.subplots(3, 2).flatten()
    test_axes[0].stairs(y, x, baseline=None)
    test_axes[1].stairs(y, x, baseline=None, orientation='horizontal')
    test_axes[2].stairs(y, x)
    test_axes[3].stairs(y, x, orientation='horizontal')
    test_axes[4].stairs(y, x)
    test_axes[4].semilogy()
    test_axes[5].stairs(y, x, orientation='horizontal')
    test_axes[5].semilogx()

    # defaults of `PathPatch` to be used for all following Line2D
    style = {'solid_joinstyle': 'miter', 'solid_capstyle': 'butt'}

    ref_axes = fig_ref.subplots(3, 2).flatten()
    ref_axes[0].plot(x, np.append(y, y[-1]), drawstyle='steps-post', **style)
    ref_axes[1].plot(np.append(y[0], y), x, drawstyle='steps-post', **style)

    ref_axes[2].plot(x, np.append(y, y[-1]), drawstyle='steps-post', **style)
    ref_axes[2].add_line(mlines.Line2D([x[0], x[0]], [0, y[0]], **style))
    ref_axes[2].add_line(mlines.Line2D([x[-1], x[-1]], [0, y[-1]], **style))
    ref_axes[2].set_ylim(0, None)

    ref_axes[3].plot(np.append(y[0], y), x, drawstyle='steps-post', **style)
    ref_axes[3].add_line(mlines.Line2D([0, y[0]], [x[0], x[0]], **style))
    ref_axes[3].add_line(mlines.Line2D([0, y[-1]], [x[-1], x[-1]], **style))
    ref_axes[3].set_xlim(0, None)

    ref_axes[4].plot(x, np.append(y, y[-1]), drawstyle='steps-post', **style)
    ref_axes[4].add_line(mlines.Line2D([x[0], x[0]], [0, y[0]], **style))
    ref_axes[4].add_line(mlines.Line2D([x[-1], x[-1]], [0, y[-1]], **style))
    ref_axes[4].semilogy()

    ref_axes[5].plot(np.append(y[0], y), x, drawstyle='steps-post', **style)
    ref_axes[5].add_line(mlines.Line2D([0, y[0]], [x[0], x[0]], **style))
    ref_axes[5].add_line(mlines.Line2D([0, y[-1]], [x[-1], x[-1]], **style))
    ref_axes[5].semilogx()

