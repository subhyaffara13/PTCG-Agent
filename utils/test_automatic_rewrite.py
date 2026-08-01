
def test_automatic_rewrite():
    assert octave_code(Li(x)) == '(logint(x) - logint(2))'
    assert octave_code(erf2(x, y)) == '(-erf(x) + erf(y))'

