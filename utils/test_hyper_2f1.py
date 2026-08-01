
def test_hyper_2f1():
    mp.dps = 15
    v = 1.0652207633823291032
    assert hyper([(1,2), (3,4)], [2], 0.3).ae(v)
    assert hyper([(1,2), 0.75], [2], 0.3).ae(v)
    assert hyper([0.5, 0.75], [2.0], 0.3).ae(v)
    assert hyper([0.5, 0.75], [2.0], 0.3+0j).ae(v)
    assert hyper([0.5+0j, (3,4)], [2.0], 0.3+0j).ae(v)
    assert hyper([0.5+0j, (3,4)], [2.0], 0.3).ae(v)
    assert hyper([0.5, (3,4)], [2.0+0j], 0.3).ae(v)
    assert hyper([0.5+0j, 0.75+0j], [2.0+0j], 0.3+0j).ae(v)
    v = 1.09234681096223231717 + 0.18104859169479360380j
    assert hyper([(1,2),0.75+j], [2], 0.5).ae(v)
    assert hyper([0.5,0.75+j], [2.0], 0.5).ae(v)
    assert hyper([0.5,0.75+j], [2.0], 0.5+0j).ae(v)
    assert hyper([0.5,0.75+j], [2.0+0j], 0.5+0j).ae(v)
    v = 0.9625 - 0.125j
    assert hyper([(3,2),-1],[4], 0.1+j/3).ae(v)
    assert hyper([1.5,-1.0],[4], 0.1+j/3).ae(v)
    assert hyper([1.5,-1.0],[4+0j], 0.1+j/3).ae(v)
    assert hyper([1.5+0j,-1.0+0j],[4+0j], 0.1+j/3).ae(v)
    v = 1.02111069501693445001 - 0.50402252613466859521j
    assert hyper([(2,10),(3,10)],[(4,10)],1.5).ae(v)
    assert hyper([0.2,(3,10)],[0.4+0j],1.5).ae(v)
    assert hyper([0.2,(3,10)],[0.4+0j],1.5+0j).ae(v)
    v = 0.76922501362865848528 + 0.32640579593235886194j
    assert hyper([(2,10),(3,10)],[(4,10)],4+2j).ae(v)
    assert hyper([0.2,(3,10)],[0.4+0j],4+2j).ae(v)
    assert hyper([0.2,(3,10)],[(4,10)],4+2j).ae(v)

