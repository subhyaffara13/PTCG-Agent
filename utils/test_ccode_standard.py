
def test_ccode_standard():
    assert ccode(expm1(x), standard='c99') == 'expm1(x)'
    assert ccode(nan, standard='c99') == 'NAN'
    assert ccode(float('nan'), standard='c99') == 'NAN'

