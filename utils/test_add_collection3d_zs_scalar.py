
def test_add_collection3d_zs_scalar():
    theta = np.linspace(0, 2 * np.pi, 100)
    z = 1
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)

    points = np.column_stack([x, y]).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    norm = plt.Normalize(0, 2*np.pi)
    lc = LineCollection(segments, cmap='twilight', norm=norm)
    lc.set_array(theta)
    line = ax.add_collection3d(lc, zs=z)

    assert line is not None

    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    ax.set_xlim(-5, 5)
    ax.set_ylim(-4, 6)
    ax.set_zlim(0, 2)

