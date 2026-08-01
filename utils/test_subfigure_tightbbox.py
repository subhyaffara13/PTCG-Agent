
def test_subfigure_tightbbox():
    # test that we can get the tightbbox with a subfigure...
    fig = plt.figure(layout='constrained')
    sub = fig.subfigures(1, 2)

    np.testing.assert_allclose(
            fig.get_tightbbox(fig.canvas.get_renderer()).width,
            8.0)

