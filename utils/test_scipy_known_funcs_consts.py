
def test_scipy_known_funcs_consts():
    assert _scipy_known_constants['GoldenRatio'] == 'scipy.constants.golden_ratio'
    assert _scipy_known_constants['Pi'] == 'scipy.constants.pi'

    assert _scipy_known_functions['erf'] == 'scipy.special.erf'
    assert _scipy_known_functions['factorial'] == 'scipy.special.factorial'

