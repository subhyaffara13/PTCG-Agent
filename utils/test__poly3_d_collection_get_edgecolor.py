
def test_Poly3DCollection_get_edgecolor():
    # Smoke test to see that get_edgecolor does not raise
    # See GH#4067
    y, x = np.ogrid[1:10:100j, 1:10:100j]
    z2 = np.cos(x) ** 3 - np.sin(y) ** 2
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r = ax.plot_surface(x, y, z2, cmap='hot')
    r.get_edgecolor()

