
def test_jax_known_funcs_consts():
    assert _jax_known_constants['NaN'] == 'jax.numpy.nan'
    assert _jax_known_constants['EulerGamma'] == 'jax.numpy.euler_gamma'

    assert _jax_known_functions['acos'] == 'jax.numpy.arccos'
    assert _jax_known_functions['log'] == 'jax.numpy.log'

