
def test_hyper_2f1_hard():
    mp.dps = 15
    # Singular cases
    assert hyp2f1(2,-1,-1,3).ae(7)
    assert hyp2f1(2,-1,-1,3,eliminate_all=True).ae(0.25)
    assert hyp2f1(2,-2,-2,3).ae(34)
    assert hyp2f1(2,-2,-2,3,eliminate_all=True).ae(0.25)
    assert hyp2f1(2,-2,-3,3) == 14
    assert hyp2f1(2,-3,-2,3) == inf
    assert hyp2f1(2,-1.5,-1.5,3) == 0.25
    assert hyp2f1(1,2,3,0) == 1
    assert hyp2f1(0,1,0,0) == 1
    assert hyp2f1(0,0,0,0) == 1
    assert isnan(hyp2f1(1,1,0,0))
    assert hyp2f1(2,-1,-5, 0.25+0.25j).ae(1.1+0.1j)
    assert hyp2f1(2,-5,-5, 0.25+0.25j, eliminate=False).ae(163./128 + 125./128*j)
    assert hyp2f1(0.7235, -1, -5, 0.3).ae(1.04341)
    assert hyp2f1(0.7235, -5, -5, 0.3, eliminate=False).ae(1.2939225017815903812)
    assert hyp2f1(-1,-2,4,1) == 1.5
    assert hyp2f1(1,2,-3,1) == inf
    assert hyp2f1(-2,-2,1,1) == 6
    assert hyp2f1(1,-2,-4,1).ae(5./3)
    assert hyp2f1(0,-6,-4,1) == 1
    assert hyp2f1(0,-3,-4,1) == 1
    assert hyp2f1(0,0,0,1) == 1
    assert hyp2f1(1,0,0,1,eliminate=False) == 1
    assert hyp2f1(1,1,0,1) == inf
    assert hyp2f1(1,-6,-4,1) == inf
    assert hyp2f1(-7.2,-0.5,-4.5,1) == 0
    assert hyp2f1(-7.2,-1,-2,1).ae(-2.6)
    assert hyp2f1(1,-0.5,-4.5, 1) == inf
    assert hyp2f1(1,0.5,-4.5, 1) == -inf
    # Check evaluation on / close to unit circle
    z = exp(j*pi/3)
    w = (nthroot(2,3)+1)*exp(j*pi/12)/nthroot(3,4)**3
    assert hyp2f1('1/2','1/6','1/3', z).ae(w)
    assert hyp2f1('1/2','1/6','1/3', z.conjugate()).ae(w.conjugate())
    assert hyp2f1(0.25, (1,3), 2, '0.999').ae(1.06826449496030635)
    assert hyp2f1(0.25, (1,3), 2, '1.001').ae(1.06867299254830309446-0.00001446586793975874j)
    assert hyp2f1(0.25, (1,3), 2, -1).ae(0.96656584492524351673)
    assert hyp2f1(0.25, (1,3), 2, j).ae(0.99041766248982072266+0.03777135604180735522j)
    assert hyp2f1(2,3,5,'0.99').ae(27.699347904322690602)
    assert hyp2f1((3,2),-0.5,3,'0.99').ae(0.68403036843911661388)
    assert hyp2f1(2,3,5,1j).ae(0.37290667145974386127+0.59210004902748285917j)
    assert fsum([hyp2f1((7,10),(2,3),(-1,2), 0.95*exp(j*k)) for k in range(1,15)]).ae(52.851400204289452922+6.244285013912953225j)
    assert fsum([hyp2f1((7,10),(2,3),(-1,2), 1.05*exp(j*k)) for k in range(1,15)]).ae(54.506013786220655330-3.000118813413217097j)
    assert fsum([hyp2f1((7,10),(2,3),(-1,2), exp(j*k)) for k in range(1,15)]).ae(55.792077935955314887+1.731986485778500241j)
    assert hyp2f1(2,2.5,-3.25,0.999).ae(218373932801217082543180041.33)
    # Branches
    assert hyp2f1(1,1,2,1.01).ae(4.5595744415723676911-3.1104877758314784539j)
    assert hyp2f1(1,1,2,1.01+0.1j).ae(2.4149427480552782484+1.4148224796836938829j)
    assert hyp2f1(1,1,2,3+4j).ae(0.14576709331407297807+0.48379185417980360773j)
    assert hyp2f1(1,1,2,4).ae(-0.27465307216702742285 - 0.78539816339744830962j)
    assert hyp2f1(1,1,2,-4).ae(0.40235947810852509365)
    # Other:
    # Cancellation with a large parameter involved (bug reported on sage-devel)
    assert hyp2f1(112, (51,10), (-9,10), -0.99999).ae(-1.6241361047970862961e-24, abs_eps=0, rel_eps=eps*16)

