
def test_arc_ellipse():
    xcenter, ycenter = 0.38, 0.52
    width, height = 1e-1, 3e-1
    angle = -30

    theta = np.deg2rad(np.arange(360))
    x = width / 2. * np.cos(theta)
    y = height / 2. * np.sin(theta)

    rtheta = np.deg2rad(angle)
    R = np.array([
        [np.cos(rtheta), -np.sin(rtheta)],
        [np.sin(rtheta), np.cos(rtheta)]])

    x, y = np.dot(R, [x, y])
    x += xcenter
    y += ycenter

    fig = plt.figure()
    ax = fig.add_subplot(211, aspect='auto')
    ax.fill(x, y, alpha=0.2, facecolor='yellow', edgecolor='yellow',
            linewidth=1, zorder=1)

    e1 = mpatches.Arc((xcenter, ycenter), width, height,
                      angle=angle, linewidth=2, fill=False, zorder=2)

    ax.add_patch(e1)

    ax = fig.add_subplot(212, aspect='equal')
    ax.fill(x, y, alpha=0.2, facecolor='green', edgecolor='green', zorder=1)
    e2 = mpatches.Arc((xcenter, ycenter), width, height,
                      angle=angle, linewidth=2, fill=False, zorder=2)

    ax.add_patch(e2)

