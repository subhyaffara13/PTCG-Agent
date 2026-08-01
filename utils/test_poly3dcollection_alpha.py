
def test_poly3dcollection_alpha():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    poly1 = np.array([[0, 0, 1], [0, 1, 1], [0, 0, 0]], float)
    poly2 = np.array([[0, 1, 1], [1, 1, 1], [1, 1, 0]], float)
    c1 = art3d.Poly3DCollection([poly1], linewidths=3, edgecolor='k',
                                facecolor=(0.5, 0.5, 1), closed=True)
    c1.set_alpha(0.5)
    c2 = art3d.Poly3DCollection([poly2], linewidths=3, closed=False)
    # Post-creation modification should work.
    c2.set_facecolor((1, 0.5, 0.5))
    c2.set_edgecolor('k')
    c2.set_alpha(0.5)
    ax.add_collection3d(c1, autolim=False)
    ax.add_collection3d(c2, autolim=False)

