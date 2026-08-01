
def test_submerged_height_gap():
    """Test that the gap between rows does not depend on the number of columns."""

    mosaic1 = "AC;BC"
    mosaic2 = "ACDE;BCDE"

    fig1, ax_dict1 = plt.subplot_mosaic(mosaic1, layout='constrained')
    fig2, ax_dict2 = plt.subplot_mosaic(mosaic2, layout='constrained')
    for fig in fig1, fig2:
        fig.get_layout_engine().set(h_pad=0.2)
        fig.draw_without_rendering()

    for label in 'A', 'B':
        np.testing.assert_allclose(ax_dict1[label].get_position().bounds[-1],
                                   ax_dict2[label].get_position().bounds[-1])

