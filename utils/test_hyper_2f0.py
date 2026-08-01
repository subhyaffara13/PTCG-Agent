
def test_hyper_2f0():
    mp.dps = 15
    assert hyper([1,2],[],3) == hyp2f0(1,2,3)
    assert hyp2f0(2,3,7).ae(0.0116108068639728714668 - 0.0073727413865865802130j)
    assert hyp2f0(2,3,0) == 1
    assert hyp2f0(0,0,0) == 1
    assert hyp2f0(-1,-1,1).ae(2)
    assert hyp2f0(-4,1,1.5).ae(62.5)
    assert hyp2f0(-4,1,50).ae(147029801)
    assert hyp2f0(-4,1,0.0001).ae(0.99960011997600240000)
    assert hyp2f0(0.5,0.25,0.001).ae(1.0001251174078538115)
    assert hyp2f0(0.5,0.25,3+4j).ae(0.85548875824755163518 + 0.21636041283392292973j)
    # Important: cancellation check
    assert hyp2f0((1,6),(5,6),-0.02371708245126284498).ae(0.996785723120804309)
    # Should be exact; polynomial case
    assert hyp2f0(-2,1,0.5+0.5j,zeroprec=200) == 0
    assert hyp2f0(1,-2,0.5+0.5j,zeroprec=200) == 0
    # There used to be a bug in thresholds that made one of the following hang
    for d in [15, 50, 80]:
        mp.dps = d
        assert hyp2f0(1.5, 0.5, 0.009).ae('1.006867007239309717945323585695344927904000945829843527398772456281301440034218290443367270629519483 + 1.238277162240704919639384945859073461954721356062919829456053965502443570466701567100438048602352623e-46j')

