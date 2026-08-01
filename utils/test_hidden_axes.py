
def test_hidden_axes():
    # test that if we make an Axes not visible that constrained_layout
    # still works.  Note the axes still takes space in the layout
    # (as does a gridspec slot that is empty)
    fig, axs = plt.subplots(2, 2, layout="constrained")
    axs[0, 1].set_visible(False)
    fig.draw_without_rendering()
    extents1 = np.copy(axs[0, 0].get_position().extents)

    np.testing.assert_allclose(
        extents1, [0.046918, 0.541204, 0.477409, 0.980555], rtol=1e-5)

