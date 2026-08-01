
def test_mixedsubplots():
    def f(t):
        return np.cos(2*np.pi*t) * np.exp(-t)

    t1 = np.arange(0.0, 5.0, 0.1)
    t2 = np.arange(0.0, 5.0, 0.02)

    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure(figsize=plt.figaspect(2.))
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(t1, f(t1), 'bo', t2, f(t2), 'k--', markerfacecolor='green')
    ax.grid(True)

    ax = fig.add_subplot(2, 1, 2, projection='3d')
    X, Y = np.meshgrid(np.arange(-5, 5, 0.25), np.arange(-5, 5, 0.25))
    R = np.hypot(X, Y)
    Z = np.sin(R)

    ax.plot_surface(X, Y, Z, rcount=40, ccount=40,
                    linewidth=0, antialiased=False)

    ax.set_zlim3d(-1, 1)

