
def test_get_math_macros():
    macros = get_math_macros()
    assert macros[exp(1)] == 'M_E'
    assert macros[1/Sqrt(2)] == 'M_SQRT1_2'

