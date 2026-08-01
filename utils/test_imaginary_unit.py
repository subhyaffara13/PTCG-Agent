
def test_imaginary_unit():
    assert latex(1 + I) == r'1 + i'
    assert latex(1 + I, imaginary_unit='i') == r'1 + i'
    assert latex(1 + I, imaginary_unit='j') == r'1 + j'
    assert latex(1 + I, imaginary_unit='foo') == r'1 + foo'
    assert latex(I, imaginary_unit="ti") == r'\text{i}'
    assert latex(I, imaginary_unit="tj") == r'\text{j}'


def test_imaginary_unit():
    from sympy.printing.pretty import pretty  # b/c it was redefined above
    assert pretty(1 + I, use_unicode=False) == '1 + I'
    assert pretty(1 + I, use_unicode=True) == '1 + ⅈ'
    assert pretty(1 + I, use_unicode=False, imaginary_unit='j') == '1 + I'
    assert pretty(1 + I, use_unicode=True, imaginary_unit='j') == '1 + ⅉ'

    raises(TypeError, lambda: pretty(I, imaginary_unit=I))
    raises(ValueError, lambda: pretty(I, imaginary_unit="kkk"))

