
def test_hyper_u():
    mp.dps = 15
    assert hyperu(2,-3,0).ae(0.05)
    assert hyperu(2,-3.5,0).ae(4./99)
    assert hyperu(2,0,0) == 0.5
    assert hyperu(-5,1,0) == -120
    assert hyperu(-5,2,0) == inf
    assert hyperu(-5,-2,0) == 0
    assert hyperu(7,7,3).ae(0.00014681269365593503986)  #exp(3)*gammainc(-6,3)
    assert hyperu(2,-3,4).ae(0.011836478100271995559)
    assert hyperu(3,4,5).ae(1./125)
    assert hyperu(2,3,0.0625) == 256
    assert hyperu(-1,2,0.25+0.5j) == -1.75+0.5j
    assert hyperu(0.5,1.5,7.25).ae(2/sqrt(29))
    assert hyperu(2,6,pi).ae(0.55804439825913399130)
    assert (hyperu((3,2),8,100+201j)*10**4).ae(-0.3797318333856738798 - 2.9974928453561707782j)
    assert (hyperu((5,2),(-1,2),-5000)*10**10).ae(-5.6681877926881664678j)

