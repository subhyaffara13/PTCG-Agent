
def test_contour_colorbar():
    x, y, z = contour_dat()

    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, z, levels=np.arange(-1.8, 1.801, 0.2),
                     cmap=mpl.colormaps['RdBu'],
                     vmin=-0.6,
                     vmax=0.6,
                     extend='both')
    cs1 = ax.contour(x, y, z, levels=np.arange(-2.2, -0.599, 0.2),
                     colors=['y'],
                     linestyles='solid',
                     linewidths=2)
    cs2 = ax.contour(x, y, z, levels=np.arange(0.6, 2.2, 0.2),
                     colors=['c'],
                     linewidths=2)
    cbar = fig.colorbar(cs, ax=ax)
    cbar.add_lines(cs1)
    cbar.add_lines(cs2, erase=False)


def test_contour_colorbar():
    fig, ax = plt.subplots(figsize=(4, 2))
    data = np.arange(1200).reshape(30, 40) - 500
    levels = np.array([0, 200, 400, 600, 800, 1000, 1200]) - 500

    CS = ax.contour(data, levels=levels, extend='both')
    fig.colorbar(CS, orientation='horizontal', extend='both')
    fig.colorbar(CS, orientation='vertical')

