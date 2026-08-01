
def test_stem3d():
    fig, axs = plt.subplots(2, 3, figsize=(8, 6),
                            constrained_layout=True,
                            subplot_kw={'projection': '3d'})

    theta = np.linspace(0, 2*np.pi)
    x = np.cos(theta - np.pi/2)
    y = np.sin(theta - np.pi/2)
    z = theta

    for ax, zdir in zip(axs[0], ['x', 'y', 'z']):
        ax.stem(x, y, z, orientation=zdir)
        ax.set_title(f'orientation={zdir}')

    x = np.linspace(-np.pi/2, np.pi/2, 20)
    y = np.ones_like(x)
    z = np.cos(x)

    for ax, zdir in zip(axs[1], ['x', 'y', 'z']):
        markerline, stemlines, baseline = ax.stem(
            x, y, z,
            linefmt='C4-.', markerfmt='C1D', basefmt='C2',
            orientation=zdir)
        ax.set_title(f'orientation={zdir}')
        markerline.set(markerfacecolor='none', markeredgewidth=2)
        baseline.set_linewidth(3)

