
def test_twoslope_colorbar():
    # Note that the second tick = 20, and should be in the middle
    # of the colorbar (white)
    # There should be no tick right at the bottom, nor at the top.
    fig, ax = plt.subplots()

    norm = mcolors.TwoSlopeNorm(20, 5, 95)
    pc = ax.pcolormesh(np.arange(1, 11), np.arange(1, 11),
                       np.arange(100).reshape(10, 10),
                       norm=norm, cmap='RdBu_r')
    fig.colorbar(pc)

