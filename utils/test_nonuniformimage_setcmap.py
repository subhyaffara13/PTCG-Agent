
def test_nonuniformimage_setcmap():
    ax = plt.gca()
    im = NonUniformImage(ax)
    im.set_cmap('Blues')

