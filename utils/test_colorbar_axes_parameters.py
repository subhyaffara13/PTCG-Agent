
def test_colorbar_axes_parameters():
    fig, ax = plt.subplots(2)
    im = ax[0].imshow([[0, 1], [2, 3]])
    # colorbar should accept any form of axes sequence:
    fig.colorbar(im, ax=ax)
    fig.colorbar(im, ax=ax[0])
    fig.colorbar(im, ax=[_ax for _ax in ax])
    fig.colorbar(im, ax=(ax[0], ax[1]))
    fig.colorbar(im, ax={i: _ax for i, _ax in enumerate(ax)}.values())
    fig.draw_without_rendering()

