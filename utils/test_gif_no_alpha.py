
def test_gif_no_alpha():
    plt.plot([0, 1, 2], [0, 1, 0])
    buf = io.BytesIO()
    plt.savefig(buf, format="gif", transparent=False)
    im = Image.open(buf)
    assert im.mode == "P"
    assert im.info["transparency"] >= len(im.palette.colors)

