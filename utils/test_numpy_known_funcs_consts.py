
def test_numpy_known_funcs_consts():
    assert _numpy_known_constants['NaN'] == 'numpy.nan'
    assert _numpy_known_constants['EulerGamma'] == 'numpy.euler_gamma'

    assert _numpy_known_functions['acos'] == 'numpy.arccos'
    assert _numpy_known_functions['log'] == 'numpy.log'

