
def test_axhvlinespan_interpolation():
    ax = plt.figure().add_subplot(projection="polar")
    ax.set_axis_off()
    ax.axvline(.1, c="C0")
    ax.axvspan(.2, .3, fc="C1")
    ax.axvspan(.4, .5, .1, .2, fc="C2")
    ax.axhline(1, c="C0", alpha=.5)
    ax.axhspan(.8, .9, fc="C1", alpha=.5)
    ax.axhspan(.6, .7, .8, .9, fc="C2", alpha=.5)

