
def test_mask_image_all():
    # Test behavior with an image that is entirely masked does not warn
    data = np.full((2, 2), np.nan)
    fig, ax = plt.subplots()
    ax.imshow(data)
    fig.canvas.draw_idle()  # would emit a warning

