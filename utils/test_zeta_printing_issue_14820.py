
def test_zeta_printing_issue_14820():
    assert octave_code(zeta(x)) == 'zeta(x)'
    with raises(NotImplementedError):
        octave_code(zeta(x, y))

