
def test_clipper():
    dat = (0, 1, 0, 2, 0, 3, 0, 4, 0, 5)
    fig = plt.figure(figsize=(2, 1))
    fig.subplots_adjust(left=0, bottom=0, wspace=0, hspace=0)

    ax = fig.add_axes((0, 0, 1.0, 1.0), ylim=(0, 5), autoscale_on=False)
    ax.plot(dat)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.set_xlim(5, 9)

