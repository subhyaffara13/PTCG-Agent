
def test_sympify_text():
    assert sympify('some') == Symbol('some')
    assert sympify('core') == Symbol('core')

    assert sympify('True') is True
    assert sympify('False') is False

    assert sympify('Poly') == Poly
    assert sympify('sin') == sin

