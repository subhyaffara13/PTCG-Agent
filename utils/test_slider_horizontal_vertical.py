
def test_slider_horizontal_vertical():
    fig, ax = plt.subplots()
    slider = widgets.Slider(ax=ax, label='', valmin=0, valmax=24,
                            valinit=12, orientation='horizontal')
    slider.set_val(10)
    assert slider.val == 10
    # check the dimension of the slider patch in axes units
    box = slider.poly.get_extents().transformed(ax.transAxes.inverted())
    assert_allclose(box.bounds, [0, .25, 10/24, .5])

    fig, ax = plt.subplots()
    slider = widgets.Slider(ax=ax, label='', valmin=0, valmax=24,
                            valinit=12, orientation='vertical')
    slider.set_val(10)
    assert slider.val == 10
    # check the dimension of the slider patch in axes units
    box = slider.poly.get_extents().transformed(ax.transAxes.inverted())
    assert_allclose(box.bounds, [.25, 0, .5, 10/24])

