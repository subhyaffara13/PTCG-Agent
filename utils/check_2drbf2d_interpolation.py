
def check_2drbf2d_interpolation(function):
    # Check that the 2-D Rbf function interpolates through the nodes (2D).
    rng = np.random.RandomState(1234)
    x = rng.rand(50, ) * 4 - 2
    y = rng.rand(50, ) * 4 - 2
    z0 = x * exp(-x ** 2 - 1j * y ** 2)
    z1 = y * exp(-y ** 2 - 1j * x ** 2)
    z = np.vstack([z0, z1]).T
    rbf = Rbf(x, y, z, epsilon=2, function=function, mode='N-D')
    zi = rbf(x, y)
    zi = zi.reshape(z.shape)
    assert_array_almost_equal(z, zi)

