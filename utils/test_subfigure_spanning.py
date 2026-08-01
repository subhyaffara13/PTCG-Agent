
def test_subfigure_spanning():
    # test that subfigures get laid out properly...
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(3, 3)
    sub_figs = [
        fig.add_subfigure(gs[0, 0]),
        fig.add_subfigure(gs[0:2, 1]),
        fig.add_subfigure(gs[2, 1:3]),
        fig.add_subfigure(gs[0:, 1:])
    ]

    w = 640
    h = 480
    np.testing.assert_allclose(sub_figs[0].bbox.min, [0., h * 2/3])
    np.testing.assert_allclose(sub_figs[0].bbox.max, [w / 3, h])

    np.testing.assert_allclose(sub_figs[1].bbox.min, [w / 3, h / 3])
    np.testing.assert_allclose(sub_figs[1].bbox.max, [w * 2/3, h])

    np.testing.assert_allclose(sub_figs[2].bbox.min, [w / 3, 0])
    np.testing.assert_allclose(sub_figs[2].bbox.max, [w, h / 3])

    # check here that slicing actually works.  Last sub_fig
    # with open slices failed, but only on draw...
    for i in range(4):
        sub_figs[i].add_subplot()
    fig.draw_without_rendering()

