
def test_nonuniformimage_setnorm():
    ax = plt.gca()
    im = NonUniformImage(ax)
    im.set_norm(plt.Normalize())

