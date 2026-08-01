
def test_bbox_inches_inset_rasterized():
    fig, ax = plt.subplots()

    arr = np.arange(100).reshape(10, 10)
    im = ax.imshow(arr)
    inset = inset_axes(
        ax, width='10%', height='30%', loc='upper left',
        bbox_to_anchor=(0.045, 0., 1, 1), bbox_transform=ax.transAxes)

    fig.colorbar(im, cax=inset, orientation='horizontal')

