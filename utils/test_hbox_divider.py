
def test_hbox_divider():
    arr1 = np.arange(20).reshape((4, 5))
    arr2 = np.arange(20).reshape((5, 4))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(arr1)
    ax2.imshow(arr2)

    pad = 0.5  # inches.
    divider = HBoxDivider(
        fig, 111,  # Position of combined axes.
        horizontal=[Size.AxesX(ax1), Size.Fixed(pad), Size.AxesX(ax2)],
        vertical=[Size.AxesY(ax1), Size.Scaled(1), Size.AxesY(ax2)])
    ax1.set_axes_locator(divider.new_locator(0))
    ax2.set_axes_locator(divider.new_locator(2))

    fig.canvas.draw()
    p1 = ax1.get_position()
    p2 = ax2.get_position()
    assert p1.height == p2.height
    assert p2.width / p1.width == pytest.approx((4 / 5) ** 2)

