
def test_struve():
    mp.dps = 15
    assert struveh(2,3).ae(0.74238666967748318564)
    assert struveh(-2.5,3).ae(0.41271003220971599344)
    assert struvel(2,3).ae(1.7476573277362782744)
    assert struvel(-2.5,3).ae(1.5153394466819651377)

