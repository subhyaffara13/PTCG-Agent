
def test_hyper_0f1():
    mp.dps = 15
    v = 8.63911136507950465
    assert hyper([],[(1,3)],1.5).ae(v)
    assert hyper([],[1/3.],1.5).ae(v)
    assert hyp0f1(1/3.,1.5).ae(v)
    assert hyp0f1((1,3),1.5).ae(v)
    # Asymptotic expansion
    assert hyp0f1(3,1e9).ae('4.9679055380347771271e+27455')
    assert hyp0f1(3,1e9j).ae('-2.1222788784457702157e+19410 + 5.0840597555401854116e+19410j')

