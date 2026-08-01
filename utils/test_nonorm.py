
def test_nonorm():
    plt.rcParams['svg.fonttype'] = 'none'
    data = [1, 2, 3, 4, 5]

    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    norm = NoNorm(vmin=min(data), vmax=max(data))
    cmap = mpl.colormaps["viridis"].resampled(len(data))
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = fig.colorbar(mappable, cax=ax, orientation="horizontal")

