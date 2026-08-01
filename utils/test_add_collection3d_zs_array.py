
def test_add_collection3d_zs_array():
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)

    points = np.column_stack([x, y, z]).reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    norm = plt.Normalize(0, 2*np.pi)
    # 2D LineCollection from x & y values
    lc = LineCollection(segments[:, :, :2], cmap='twilight', norm=norm)
    lc.set_array(np.mod(theta, 2*np.pi))
    # Add 2D collection at z values to ax
    line = ax.add_collection3d(lc, zs=segments[:, :, 2])

    assert line is not None

    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    ax.set_xlim(-5, 5)
    ax.set_ylim(-4, 6)
    ax.set_zlim(-2, 2)

