
def test_pcolorargs():
    n = 12
    x = np.linspace(-1.5, 1.5, n)
    y = np.linspace(-1.5, 1.5, n*2)
    X, Y = np.meshgrid(x, y)
    Z = np.hypot(X, Y) / 5

    _, ax = plt.subplots()
    with pytest.raises(TypeError):
        ax.pcolormesh(y, x, Z)
    with pytest.raises(TypeError):
        ax.pcolormesh(X, Y, Z.T)
    with pytest.raises(TypeError):
        ax.pcolormesh(x, y, Z[:-1, :-1], shading="gouraud")
    with pytest.raises(TypeError):
        ax.pcolormesh(X, Y, Z[:-1, :-1], shading="gouraud")
    x[0] = np.nan
    with pytest.raises(ValueError):
        ax.pcolormesh(x, y, Z[:-1, :-1])
    with np.errstate(invalid='ignore'):
        x = np.ma.array(x, mask=(x < 0))
    with pytest.raises(ValueError):
        ax.pcolormesh(x, y, Z[:-1, :-1])
    # If the X or Y coords do not possess monotonicity in their respective
    # directions, a warning indicating a bad grid will be triggered.
    # The case of specifying coordinates by inputting 1D arrays.
    x = [359, 0, 1]
    y = [-10, 10]
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    with pytest.warns(UserWarning,
                      match='are not monotonically increasing or decreasing'):
        ax.pcolormesh(X, Y, Z, shading='auto')
    # The case of specifying coordinates by inputting 2D arrays.
    x = np.linspace(-1, 1, 3)
    y = np.linspace(-1, 1, 3)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    np.random.seed(19680801)
    noise_X = np.random.random(X.shape)
    noise_Y = np.random.random(Y.shape)
    with pytest.warns(UserWarning,
                      match='are not monotonically increasing or '
                            'decreasing') as record:
        # Small perturbations in coordinates will not disrupt the monotonicity
        # of the X-coords and Y-coords in their respective directions.
        # Therefore, no warnings will be triggered.
        ax.pcolormesh(X+noise_X, Y+noise_Y, Z, shading='auto')
        assert len(record) == 0
        # Large perturbations have disrupted the monotonicity of the X-coords
        # and Y-coords in their respective directions, thus resulting in two
        # bad grid warnings.
        ax.pcolormesh(X+10*noise_X, Y+10*noise_Y, Z, shading='auto')
        assert len(record) == 2

