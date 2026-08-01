
def test_SymLogNorm_colorbar():
    """
    Test un-called SymLogNorm in a colorbar.
    """
    norm = mcolors.SymLogNorm(0.1, vmin=-1, vmax=1, linscale=1, base=np.e)
    fig = plt.figure()
    mcolorbar.ColorbarBase(fig.add_subplot(), norm=norm)
    plt.close(fig)

