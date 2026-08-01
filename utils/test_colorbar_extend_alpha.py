
def test_colorbar_extend_alpha():
    fig, ax = plt.subplots()
    im = ax.imshow([[0, 1], [2, 3]], alpha=0.3, interpolation="none")
    fig.colorbar(im, extend='both', boundaries=[0.5, 1.5, 2.5])

