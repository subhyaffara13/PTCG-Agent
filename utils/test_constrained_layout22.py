
def test_constrained_layout22():
    """#11035: suptitle should not be include in CL if manually positioned"""
    fig, ax = plt.subplots(layout="constrained")

    fig.draw_without_rendering()
    extents0 = np.copy(ax.get_position().extents)

    fig.suptitle("Suptitle", y=0.5)
    fig.draw_without_rendering()
    extents1 = np.copy(ax.get_position().extents)

    np.testing.assert_allclose(extents0, extents1)

