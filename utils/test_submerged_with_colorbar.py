
def test_submerged_with_colorbar():
    mosaic = "AABBCC;DDDEEE"

    fig, ax_dict = plt.subplot_mosaic(mosaic, layout='constrained')

    cf = ax_dict['A'].contourf([[0, 1], [2, 3]])
    fig.colorbar(cf)

