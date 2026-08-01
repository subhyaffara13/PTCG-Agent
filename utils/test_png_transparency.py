
def test_png_transparency():  # Actually, also just testing that png works.
    buf = BytesIO()
    plt.figure().savefig(buf, format="png", backend="pgf", transparent=True)
    buf.seek(0)
    t = plt.imread(buf)
    assert (t[..., 3] == 0).all()  # fully transparent.

