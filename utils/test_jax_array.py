
def test_jax_array():
    assert JaxPrinter().doprint(Array(((1, 2), (3, 5)))) == 'jax.numpy.array([[1, 2], [3, 5]])'
    assert JaxPrinter().doprint(Array((1, 2))) == 'jax.numpy.array([1, 2])'

