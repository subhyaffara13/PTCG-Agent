
def check_rbf3d_interpolation(function):
    # Check that the Rbf function interpolates through the nodes (3D).
    rng = np.random.RandomState(1234)
    x = rng.rand(50, 1)*4 - 2
    y = rng.rand(50, 1)*4 - 2
    z = rng.rand(50, 1)*4 - 2
    d = x*exp(-x**2 - y**2)
    rbf = Rbf(x, y, z, d, epsilon=2, function=function)
    di = rbf(x, y, z)
    di = di.reshape(x.shape)
    assert_array_almost_equal(di, d)

