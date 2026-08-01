
def check_2drbf3d_interpolation(function):
    # Check that the 2-D Rbf function interpolates through the nodes (3D).
    rng = np.random.RandomState(1234)
    x = rng.rand(50, ) * 4 - 2
    y = rng.rand(50, ) * 4 - 2
    z = rng.rand(50, ) * 4 - 2
    d0 = x * exp(-x ** 2 - y ** 2)
    d1 = y * exp(-y ** 2 - x ** 2)
    d = np.vstack([d0, d1]).T
    rbf = Rbf(x, y, z, d, epsilon=2, function=function, mode='N-D')
    di = rbf(x, y, z)
    di = di.reshape(d.shape)
    assert_array_almost_equal(di, d)

