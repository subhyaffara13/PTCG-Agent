
def test_powernorm_cbar_limits():
    fig, ax = plt.subplots()
    vmin, vmax = 300, 1000
    data = np.arange(10*10).reshape(10, 10) + vmin
    im = ax.imshow(data, norm=mcolors.PowerNorm(gamma=0.2, vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(im)
    assert cbar.ax.get_ylim() == (vmin, vmax)

