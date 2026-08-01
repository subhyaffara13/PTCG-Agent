
def test_contour_line_start_on_corner_edge():
    fig, ax = plt.subplots(figsize=(6, 5))

    x, y = np.meshgrid([0, 1, 2, 3, 4], [0, 1, 2])
    z = 1.2 - (x - 2)**2 + (y - 1)**2
    mask = np.zeros_like(z, dtype=bool)
    mask[1, 1] = mask[1, 3] = True
    z = np.ma.array(z, mask=mask)

    filled = ax.contourf(x, y, z, corner_mask=True)
    cbar = fig.colorbar(filled)
    lines = ax.contour(x, y, z, corner_mask=True, colors='k')
    cbar.add_lines(lines)

