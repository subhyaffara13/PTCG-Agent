
def test_fill_between_polygon():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    theta = np.linspace(0, 2*np.pi, 50)

    x1 = x2 = theta
    y1 = y2 = 0
    z1 = np.cos(theta)
    z2 = z1 + 1

    where = (theta < np.pi/2) | (theta > 3*np.pi/2)

    # Since x1 == x2 and y1 == y2, the fill_between mode will be 'polygon'
    ax.fill_between(x1, y1, z1, x2, y2, z2,
                    where=where, mode='auto', edgecolor='k')

