
def test_harmonic_evalf():
    assert str(harmonic(1.5).evalf(n=10)) == '1.280372306'
    assert str(harmonic(1.5, 2).evalf(n=10)) == '1.154576311'  # issue 7443
    assert str(harmonic(4.0, -3).evalf(n=10)) == '100.0000000'
    assert str(harmonic(7.0, 1.0).evalf(n=10)) == '2.592857143'
    assert str(harmonic(1, pi).evalf(n=10)) == '1.000000000'
    assert str(harmonic(2, pi).evalf(n=10)) == '1.113314732'
    assert str(harmonic(1000.0, pi).evalf(n=10)) == '1.176241563'
    assert str(harmonic(I).evalf(n=10)) == '0.6718659855 + 1.076674047*I'
    assert str(harmonic(I, I).evalf(n=10)) == '-0.3970915266 + 1.9629689*I'

    assert harmonic(-1.0, 1).evalf() is S.NaN
    assert harmonic(-2.0, 2.0).evalf() is S.NaN

