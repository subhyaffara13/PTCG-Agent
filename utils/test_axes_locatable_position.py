
def test_axes_locatable_position():
    fig, ax = plt.subplots()
    divider = make_axes_locatable(ax)
    with mpl.rc_context({"figure.subplot.wspace": 0.02}):
        cax = divider.append_axes('right', size='5%')
    fig.canvas.draw()
    assert np.isclose(cax.get_position(original=False).width,
                      0.03621495327102808)

