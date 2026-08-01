
def test_pre_transform_plotting():
    # a catch-all for as many as possible plot layouts which handle
    # pre-transforming the data NOTE: The axis range is important in this
    # plot. It should be x10 what the data suggests it should be

    ax = plt.axes()
    times10 = mtransforms.Affine2D().scale(10)

    ax.contourf(np.arange(48).reshape(6, 8), transform=times10 + ax.transData)

    ax.pcolormesh(np.linspace(0, 4, 7),
                  np.linspace(5.5, 8, 9),
                  np.arange(48).reshape(8, 6),
                  transform=times10 + ax.transData)

    ax.scatter(np.linspace(0, 10), np.linspace(10, 0),
               transform=times10 + ax.transData)

    x = np.linspace(8, 10, 20)
    y = np.linspace(1, 5, 20)
    u = 2*np.sin(x) + np.cos(y[:, np.newaxis])
    v = np.sin(x) - np.cos(y[:, np.newaxis])

    ax.streamplot(x, y, u, v, transform=times10 + ax.transData,
                  linewidth=np.hypot(u, v))

    # reduce the vector data down a bit for barb and quiver plotting
    x, y = x[::3], y[::3]
    u, v = u[::3, ::3], v[::3, ::3]

    ax.quiver(x, y + 5, u, v, transform=times10 + ax.transData)

    ax.barbs(x - 3, y + 5, u**2, v**2, transform=times10 + ax.transData)

