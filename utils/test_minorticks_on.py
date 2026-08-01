
def test_minorticks_on(xscale, yscale):
    ax = plt.subplot()
    ax.plot([1, 2, 3, 4])
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ax.minorticks_on()

