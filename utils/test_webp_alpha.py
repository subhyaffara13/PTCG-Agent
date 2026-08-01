
def test_webp_alpha():
    plt.plot([0, 1, 2], [0, 1, 0])
    buf = io.BytesIO()
    plt.savefig(buf, format="webp", transparent=True)
    im = Image.open(buf)
    assert im.mode == "RGBA"

