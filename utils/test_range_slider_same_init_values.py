
def test_range_slider_same_init_values(orientation):
    if orientation == "vertical":
        idx = [1, 0, 3, 2]
    else:
        idx = [0, 1, 2, 3]

    fig, ax = plt.subplots()

    slider = widgets.RangeSlider(
         ax=ax, label="", valmin=0.0, valmax=1.0, orientation=orientation,
         valinit=[0, 0]
     )
    box = slider.poly.get_extents().transformed(ax.transAxes.inverted())
    assert_allclose(box.get_points().flatten()[idx], [0, 0.25, 0, 0.75])

