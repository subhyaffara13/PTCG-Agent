
def test_strip_math():
    assert strip_math(r'1 \times 2') == r'1 \times 2'
    assert strip_math(r'$1 \times 2$') == '1 x 2'
    assert strip_math(r'$\rm{hi}$') == 'hi'

