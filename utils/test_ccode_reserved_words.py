
def test_ccode_reserved_words():
    x, y = symbols('x, if')
    with raises(ValueError):
        ccode(y**2, error_on_reserved=True, standard='C99')
    assert ccode(y**2) == 'pow(if_, 2)'
    assert ccode(x * y**2, dereference=[y]) == 'pow((*if_), 2)*x'
    assert ccode(y**2, reserved_word_suffix='_unreserved') == 'pow(if_unreserved, 2)'

