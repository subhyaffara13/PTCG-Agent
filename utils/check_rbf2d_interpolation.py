
def check_rbf2d_interpolation(function):
    # Check that the Rbf function interpolates through the nodes (2D).
    rng = np.random.RandomState(1234)
    x = rng.rand(50,1)*4-2
    y = rng.rand(50,1)*4-2
    z = x*exp(-x**2-1j*y**2)
    rbf = Rbf(x, y, z, epsilon=2, function=function)
    zi = rbf(x, y)
    zi = zi.reshape(x.shape)
    assert_array_almost_equal(z, zi)

