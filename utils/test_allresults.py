
def test_allresults():
    # square = lambda x: x**2

    assert set(allresults(inc)(3)) == {inc(3)}
    assert set(allresults([inc, dec])(3)) == {2, 4}
    assert set(allresults((inc, dec))(3)) == {3}
    assert set(allresults([inc, (dec, double)])(4)) == {5, 6}

