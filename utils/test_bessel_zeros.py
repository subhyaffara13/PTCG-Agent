
def test_bessel_zeros():
    mp.dps = 15
    assert besseljzero(0,1).ae(2.40482555769577276869)
    assert besseljzero(2,1).ae(5.1356223018406825563)
    assert besseljzero(1,50).ae(157.86265540193029781)
    assert besseljzero(10,1).ae(14.475500686554541220)
    assert besseljzero(0.5,3).ae(9.4247779607693797153)
    assert besseljzero(2,1,1).ae(3.0542369282271403228)
    assert besselyzero(0,1).ae(0.89357696627916752158)
    assert besselyzero(2,1).ae(3.3842417671495934727)
    assert besselyzero(1,50).ae(156.29183520147840108)
    assert besselyzero(10,1).ae(12.128927704415439387)
    assert besselyzero(0.5,3).ae(7.8539816339744830962)
    assert besselyzero(2,1,1).ae(5.0025829314460639452)

