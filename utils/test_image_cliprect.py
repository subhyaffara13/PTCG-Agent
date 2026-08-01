
def test_image_cliprect():
    fig, ax = plt.subplots()
    d = [[1, 2], [3, 4]]

    im = ax.imshow(d, extent=(0, 5, 0, 5))

    rect = patches.Rectangle(
        xy=(1, 1), width=2, height=2, transform=im.axes.transData)
    im.set_clip_path(rect)

