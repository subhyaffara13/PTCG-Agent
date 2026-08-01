
def test_legenp():
    mp.dps = 15
    assert legenp(2,0,4) == legendre(2,4)
    assert legenp(-2, -1, 0.5).ae(0.43301270189221932338)
    assert legenp(-2, -1, 0.5, type=3).ae(0.43301270189221932338j)
    assert legenp(-2, 1, 0.5).ae(-0.86602540378443864676)
    assert legenp(2+j, 3+4j, -j).ae(134742.98773236786148 + 429782.72924463851745j)
    assert legenp(2+j, 3+4j, -j, type=3).ae(802.59463394152268507 - 251.62481308942906447j)
    assert legenp(2,4,3).ae(0)
    assert legenp(2,4,3,type=3).ae(0)
    assert legenp(2,1,0.5).ae(-1.2990381056766579701)
    assert legenp(2,1,0.5,type=3).ae(1.2990381056766579701j)
    assert legenp(3,2,3).ae(-360)
    assert legenp(3,3,3).ae(240j*2**0.5)
    assert legenp(3,4,3).ae(0)
    assert legenp(0,0.5,2).ae(0.52503756790433198939 - 0.52503756790433198939j)
    assert legenp(-1,-0.5,2).ae(0.60626116232846498110 + 0.60626116232846498110j)
    assert legenp(-2,0.5,2).ae(1.5751127037129959682 - 1.5751127037129959682j)
    assert legenp(-2,0.5,-0.5).ae(-0.85738275810499171286)

