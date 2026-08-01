
def test_contour_hatching():
    x, y, z = contour_dat()
    fig, ax = plt.subplots()
    ax.contourf(x, y, z, 7, hatches=['/', '\\', '//', '-'],
                cmap=mpl.colormaps['gray'].with_alpha(0.5),
                extend='both')

