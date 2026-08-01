
def test_fill_between_quad():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    theta = np.linspace(0, 2*np.pi, 50)

    x1 = np.cos(theta)
    y1 = np.sin(theta)
    z1 = 0.1 * np.sin(6 * theta)

    x2 = 0.6 * np.cos(theta)
    y2 = 0.6 * np.sin(theta)
    z2 = 2

    where = (theta < np.pi/2) | (theta > 3*np.pi/2)

    # Since none of x1 == x2, y1 == y2, or z1 == z2 is True, the fill_between
    # mode will map to 'quad'
    ax.fill_between(x1, y1, z1, x2, y2, z2,
                    where=where, mode='auto', alpha=0.5, edgecolor='k')

