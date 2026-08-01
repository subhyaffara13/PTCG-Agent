
def params_1(f, bounded=False):
    a = 5.0
    b = np.arange(2.0, 12.0)
    c = np.arange(2.0, 102.0).reshape((10, 10))
    d = np.arange(2.0, 1002.0).reshape((10, 10, 10))
    e = np.array([2.0, 3.0])
    g = np.arange(2.0, 12.0).reshape((1, 10, 1))
    if bounded:
        a = 0.5
        b = b / (1.5 * b.max())
        c = c / (1.5 * c.max())
        d = d / (1.5 * d.max())
        e = e / (1.5 * e.max())
        g = g / (1.5 * g.max())

    # Scalar
    f(a)
    # Scalar - size
    f(a, size=(10, 10))
    # 1d
    f(b)
    # 2d
    f(c)
    # 3d
    f(d)
    # 1d size
    f(b, size=10)
    # 2d - size - broadcast
    f(e, size=(10, 2))
    # 3d - size
    f(g, size=(10, 10, 10))

