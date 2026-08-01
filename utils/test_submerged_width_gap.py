
def test_submerged_width_gap():
    """Test that the gap between columns does not depend on the number of rows."""

    mosaic1 = "AB;CC"
    mosaic2 = "AB;CC;DD"

    fig1, ax_dict1 = plt.subplot_mosaic(mosaic1, layout='constrained')
    fig2, ax_dict2 = plt.subplot_mosaic(mosaic2, layout='constrained')
    for fig in fig1, fig2:
        fig.get_layout_engine().set(w_pad=0.2)
        fig.draw_without_rendering()

    for label in 'A', 'B':
        np.testing.assert_allclose(ax_dict1[label].get_position().bounds[-2],
                                   ax_dict2[label].get_position().bounds[-2])

