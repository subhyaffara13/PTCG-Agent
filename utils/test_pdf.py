
def test_pdf():
    mp.dps = 15
    assert npdf(-inf) == 0
    assert npdf(inf) == 0
    assert npdf(5,0,2).ae(npdf(5+4,4,2))
    assert quadts(lambda x: npdf(x,-0.5,0.8), [-inf, inf]) == 1
    assert ncdf(0) == 0.5
    assert ncdf(3,3) == 0.5
    assert ncdf(-inf) == 0
    assert ncdf(inf) == 1
    assert ncdf(10) == 1
    # Verify that this is computed accurately
    assert (ncdf(-10)*10**24).ae(7.619853024160526)

