
def test_empty_imshow(make_norm):
    fig, ax = plt.subplots()
    with pytest.warns(UserWarning,
                      match="Attempting to set identical low and high xlims"):
        im = ax.imshow([[]], norm=make_norm())
    im.set_extent([-5, 5, -5, 5])
    fig.canvas.draw()

    with pytest.raises(RuntimeError):
        im.make_image(fig.canvas.get_renderer())

