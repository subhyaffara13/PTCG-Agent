
def test_ccode_Max_Min():
    assert ccode(Max(x, 0), standard='C89') == '((0 > x) ? 0 : x)'
    assert ccode(Max(x, 0), standard='C99') == 'fmax(0, x)'
    assert ccode(Min(x, 0, sqrt(x)), standard='c89') == (
        '((0 < ((x < sqrt(x)) ? x : sqrt(x))) ? 0 : ((x < sqrt(x)) ? x : sqrt(x)))'
    )

