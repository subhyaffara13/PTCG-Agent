
def test_jax_logaddexp():
    lae = logaddexp(a, b)
    assert JaxPrinter().doprint(lae) == 'jax.numpy.logaddexp(a, b)'
    lae2 = logaddexp2(a, b)
    assert JaxPrinter().doprint(lae2) == 'jax.numpy.logaddexp2(a, b)'

