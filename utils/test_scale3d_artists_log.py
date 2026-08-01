
def test_scale3d_artists_log():
    """Test all 3D artist types with log scale."""
    fig = plt.figure(figsize=(16, 12))
    log_kw = dict(xscale='log', yscale='log', zscale='log')
    line_data = _make_log_data()
    surf_X, surf_Y, surf_Z = _make_surface_log_data()

    # Row 1: plot, wireframe, scatter, bar3d
    ax = fig.add_subplot(3, 4, 1, projection='3d')
    ax.plot(*line_data)
    ax.set(**log_kw, title='plot')

    ax = fig.add_subplot(3, 4, 2, projection='3d')
    ax.plot_wireframe(surf_X, surf_Y, surf_Z, rstride=5, cstride=5)
    ax.set(**log_kw, title='wireframe')

    ax = fig.add_subplot(3, 4, 3, projection='3d')
    ax.scatter(*line_data, c=line_data[2], cmap='viridis')
    ax.set(**log_kw, title='scatter')

    ax = fig.add_subplot(3, 4, 4, projection='3d')
    bx, by = np.meshgrid([1, 10, 100], [1, 10, 100])
    bx, by = bx.flatten(), by.flatten()
    ax.bar3d(bx, by, np.ones_like(bx, dtype=float),
             bx * 0.3, by * 0.3, bx * by / 10, alpha=0.8)
    ax.set(**log_kw, title='bar3d')

    # Row 2: surface, trisurf, contour, contourf
    ax = fig.add_subplot(3, 4, 5, projection='3d')
    ax.plot_surface(surf_X, surf_Y, surf_Z, cmap='viridis', alpha=0.8)
    ax.set(**log_kw, title='surface')

    ax = fig.add_subplot(3, 4, 6, projection='3d')
    tri_data = _make_triangulation_data()
    ax.plot_trisurf(*tri_data, cmap='viridis', alpha=0.8)
    ax.set(**log_kw, title='trisurf')

    ax = fig.add_subplot(3, 4, 7, projection='3d')
    ax.contour(surf_X, surf_Y, surf_Z, levels=10)
    ax.set(**log_kw, title='contour')

    ax = fig.add_subplot(3, 4, 8, projection='3d')
    ax.contourf(surf_X, surf_Y, surf_Z, levels=10, alpha=0.8)
    ax.set(**log_kw, title='contourf')

    # Row 3: stem, quiver, text
    ax = fig.add_subplot(3, 4, 9, projection='3d')
    ax.stem([1, 10, 100], [1, 10, 100], [10, 100, 1000], bottom=1)
    ax.set(**log_kw, title='stem')

    ax = fig.add_subplot(3, 4, 10, projection='3d')
    qxyz = np.array([1, 10, 100])
    ax.quiver(qxyz, qxyz, qxyz, qxyz * 0.5, qxyz * 0.5, qxyz * 0.5)
    ax.set(**log_kw, title='quiver')

    ax = fig.add_subplot(3, 4, 11, projection='3d')
    ax.text(1, 1, 1, "Point A")
    ax.text(10, 10, 10, "Point B")
    ax.text(100, 100, 100, "Point C")
    ax.set(**log_kw, title='text',
           xlim=(0.5, 200), ylim=(0.5, 200), zlim=(0.5, 200))

