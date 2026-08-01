
def test_FreeGroupElm_letter_form():
    assert (x**3).letter_form == (Symbol('x'), Symbol('x'), Symbol('x'))
    assert (x**2*z**-2*x).letter_form == \
        (Symbol('x'), Symbol('x'), -Symbol('z'), -Symbol('z'), Symbol('x'))

