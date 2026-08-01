
def test_exp_integrals():
    mp.dps = 15
    x = +e
    z = e + sqrt(3)*j
    assert ei(x).ae(8.21168165538361560)
    assert li(x).ae(1.89511781635593676)
    assert si(x).ae(1.82104026914756705)
    assert ci(x).ae(0.213958001340379779)
    assert shi(x).ae(4.11520706247846193)
    assert chi(x).ae(4.09647459290515367)
    assert fresnels(x).ae(0.437189718149787643)
    assert fresnelc(x).ae(0.401777759590243012)
    assert airyai(x).ae(0.0108502401568586681)
    assert airybi(x).ae(8.98245748585468627)
    assert ei(z).ae(3.72597969491314951 + 7.34213212314224421j)
    assert li(z).ae(2.28662658112562502 + 1.50427225297269364j)
    assert si(z).ae(2.48122029237669054 + 0.12684703275254834j)
    assert ci(z).ae(0.169255590269456633 - 0.892020751420780353j)
    assert shi(z).ae(1.85810366559344468 + 3.66435842914920263j)
    assert chi(z).ae(1.86787602931970484 + 3.67777369399304159j)
    assert fresnels(z/3).ae(0.034534397197008182 + 0.754859844188218737j)
    assert fresnelc(z/3).ae(1.261581645990027372 + 0.417949198775061893j)
    assert airyai(z).ae(-0.0162552579839056062 - 0.0018045715700210556j)
    assert airybi(z).ae(-4.98856113282883371 + 2.08558537872180623j)
    assert li(0) == 0.0
    assert li(1) == -inf
    assert li(inf) == inf
    assert isinstance(li(0.7), mpf)
    assert si(inf).ae(pi/2)
    assert si(-inf).ae(-pi/2)
    assert ci(inf) == 0
    assert ci(0) == -inf
    assert isinstance(ei(-0.7), mpf)
    assert airyai(inf) == 0
    assert airybi(inf) == inf
    assert airyai(-inf) == 0
    assert airybi(-inf) == 0
    assert fresnels(inf) == 0.5
    assert fresnelc(inf) == 0.5
    assert fresnels(-inf) == -0.5
    assert fresnelc(-inf) == -0.5
    assert shi(0) == 0
    assert shi(inf) == inf
    assert shi(-inf) == -inf
    assert chi(0) == -inf
    assert chi(inf) == inf

