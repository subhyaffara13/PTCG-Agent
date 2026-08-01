
def test_gettightbbox_parasite():
    fig = plt.figure()

    y0 = 0.3
    horiz = [Size.Scaled(1.0)]
    vert = [Size.Scaled(1.0)]
    ax0_div = Divider(fig, [0.1, y0, 0.8, 0.2], horiz, vert)
    ax1_div = Divider(fig, [0.1, 0.5, 0.8, 0.4], horiz, vert)

    ax0 = fig.add_subplot(
        xticks=[], yticks=[], axes_locator=ax0_div.new_locator(nx=0, ny=0))
    ax1 = fig.add_subplot(
        axes_class=HostAxes, axes_locator=ax1_div.new_locator(nx=0, ny=0))
    aux_ax = ax1.get_aux_axes(Affine2D())

    fig.canvas.draw()
    rdr = fig.canvas.get_renderer()
    assert rdr.get_canvas_width_height()[1] * y0 / fig.dpi == fig.get_tightbbox(rdr).y0

