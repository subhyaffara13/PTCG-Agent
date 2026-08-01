
def test_cupy_known_funcs_consts():
    assert _cupy_known_constants['NaN'] == 'cupy.nan'
    assert _cupy_known_constants['EulerGamma'] == 'cupy.euler_gamma'

    assert _cupy_known_functions['acos'] == 'cupy.arccos'
    assert _cupy_known_functions['log'] == 'cupy.log'

