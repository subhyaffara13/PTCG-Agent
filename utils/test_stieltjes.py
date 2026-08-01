
def test_stieltjes():
    assert isinstance(stieltjes(x), stieltjes)
    assert isinstance(stieltjes(x, a), stieltjes)

    # Zero'th constant EulerGamma
    assert stieltjes(0) == S.EulerGamma
    assert stieltjes(0, 1) == S.EulerGamma

    # Not defined
    assert stieltjes(nan) is nan
    assert stieltjes(0, nan) is nan
    assert stieltjes(-1) is S.ComplexInfinity
    assert stieltjes(1.5) is S.ComplexInfinity
    assert stieltjes(z, 0) is S.ComplexInfinity
    assert stieltjes(z, -1) is S.ComplexInfinity


def test_stieltjes():
    mp.dps = 15
    assert stieltjes(0).ae(+euler)
    mp.dps = 25
    assert stieltjes(1).ae('-0.07281584548367672486058637587')
    assert stieltjes(2).ae('-0.009690363192872318484530386035')
    assert stieltjes(3).ae('0.002053834420303345866160046543')
    assert stieltjes(4).ae('0.002325370065467300057468170178')
    mp.dps = 15
    assert stieltjes(1).ae(-0.07281584548367672486058637587)
    assert stieltjes(2).ae(-0.009690363192872318484530386035)
    assert stieltjes(3).ae(0.002053834420303345866160046543)
    assert stieltjes(4).ae(0.0023253700654673000574681701775)

