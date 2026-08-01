
def test_colorbar_shift(tmp_path):
    cmap = mcolors.ListedColormap(["r", "g", "b"])
    norm = mcolors.BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
    plt.scatter([0, 1], [1, 1], c=[0, 1], cmap=cmap, norm=norm)
    plt.colorbar()

