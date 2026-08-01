
def test_polylog():
    # log(1/x)*log(x+1)-polylog(2, -x)
    assert not integrate(log(1/x)/(x + 1), x).has(Integral)


def test_polylog():
    mp.dps = 15
    zs = [mpmathify(z) for z in [0, 0.5, 0.99, 4, -0.5, -4, 1j, 3+4j]]
    for z in zs: assert polylog(1, z).ae(-log(1-z))
    for z in zs: assert polylog(0, z).ae(z/(1-z))
    for z in zs: assert polylog(-1, z).ae(z/(1-z)**2)
    for z in zs: assert polylog(-2, z).ae(z*(1+z)/(1-z)**3)
    for z in zs: assert polylog(-3, z).ae(z*(1+4*z+z**2)/(1-z)**4)
    assert polylog(3, 7).ae(5.3192579921456754382-5.9479244480803301023j)
    assert polylog(3, -7).ae(-4.5693548977219423182)
    assert polylog(2, 0.9).ae(1.2997147230049587252)
    assert polylog(2, -0.9).ae(-0.75216317921726162037)
    assert polylog(2, 0.9j).ae(-0.17177943786580149299+0.83598828572550503226j)
    assert polylog(2, 1.1).ae(1.9619991013055685931-0.2994257606855892575j)
    assert polylog(2, -1.1).ae(-0.89083809026228260587)
    assert polylog(2, 1.1*sqrt(j)).ae(0.58841571107611387722+1.09962542118827026011j)
    assert polylog(-2, 0.9).ae(1710)
    assert polylog(-2, -0.9).ae(-90/6859.)
    assert polylog(3, 0.9).ae(1.0496589501864398696)
    assert polylog(-3, 0.9).ae(48690)
    assert polylog(-3, -4).ae(-0.0064)
    assert polylog(0.5+j/3, 0.5+j/2).ae(0.31739144796565650535 + 0.99255390416556261437j)
    assert polylog(3+4j,1).ae(zeta(3+4j))
    assert polylog(3+4j,-1).ae(-altzeta(3+4j))
    # issue 390
    assert polylog(1.5, -48.910886523731889).ae(-6.272992229311817)
    assert polylog(1.5, 200).ae(-8.349608319033686529 - 8.159694826434266042j)
    assert polylog(-2+0j, -2).ae(mpf(1)/13.5)
    assert polylog(-2+0j, 1.25).ae(-180)

