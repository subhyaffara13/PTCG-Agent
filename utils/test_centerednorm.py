
def test_centerednorm():
    # Test default centered norm gets expanded with non-singular limits
    # when plot data is all equal (autoscale halfrange == 0)
    fig, ax = plt.subplots(figsize=(1, 3))

    norm = mcolors.CenteredNorm()
    mappable = ax.pcolormesh(np.zeros((3, 3)), norm=norm)
    fig.colorbar(mappable)
    assert (norm.vmin, norm.vmax) == (-0.1, 0.1)

