
def test_gammainc():
    # Quick check that the gammainc in
    # special._precompute.gammainc_data agrees with mpmath's
    # gammainc.
    assert_mpmath_equal(gammainc,
                        lambda a, x: mp.gammainc(a, b=x, regularized=True),
                        [Arg(0, 100, inclusive_a=False), Arg(0, 100)],
                        nan_ok=False, rtol=1e-17, n=50, dps=50)


def test_gammainc():
    mp.dps = 15
    assert gammainc(2,5).ae(6*exp(-5))
    assert gammainc(2,0,5).ae(1-6*exp(-5))
    assert gammainc(2,3,5).ae(-6*exp(-5)+4*exp(-3))
    assert gammainc(-2.5,-0.5).ae(-0.9453087204829418812-5.3164237738936178621j)
    assert gammainc(0,2,4).ae(0.045121158298212213088)
    assert gammainc(0,3).ae(0.013048381094197037413)
    assert gammainc(0,2+j,1-j).ae(0.00910653685850304839-0.22378752918074432574j)
    assert gammainc(0,1-j).ae(0.00028162445198141833+0.17932453503935894015j)
    assert gammainc(3,4,5,True).ae(0.11345128607046320253)
    assert gammainc(3.5,0,inf).ae(gamma(3.5))
    assert gammainc(-150.5,500).ae('6.9825435345798951153e-627')
    assert gammainc(-150.5,800).ae('4.6885137549474089431e-788')
    assert gammainc(-3.5, -20.5).ae(0.27008820585226911 - 1310.31447140574997636j)
    assert gammainc(-3.5, -200.5).ae(0.27008820585226911 - 5.3264597096208368435e76j) # XXX real part
    assert gammainc(0,0,2) == inf
    assert gammainc(1,b=1).ae(0.6321205588285576784)
    assert gammainc(3,2,2) == 0
    assert gammainc(2,3+j,3-j).ae(-0.28135485191849314194j)
    assert gammainc(4+0j,1).ae(5.8860710587430771455)
    # GH issue #301
    assert gammainc(-1,-1).ae(-0.8231640121031084799 + 3.1415926535897932385j)
    assert gammainc(-2,-1).ae(1.7707229202810768576 - 1.5707963267948966192j)
    assert gammainc(-3,-1).ae(-1.4963349162467073643 + 0.5235987755982988731j)
    assert gammainc(-4,-1).ae(1.05365418617643814992 - 0.13089969389957471827j)
    # Regularized upper gamma
    assert isnan(gammainc(0, 0, regularized=True))
    assert gammainc(-1, 0, regularized=True) == inf
    assert gammainc(1, 0, regularized=True) == 1
    assert gammainc(0, 5, regularized=True) == 0
    assert gammainc(0, 2+3j, regularized=True) == 0
    assert gammainc(0, 5000, regularized=True) == 0
    assert gammainc(0, 10**30, regularized=True) == 0
    assert gammainc(-1, 5, regularized=True) == 0
    assert gammainc(-1, 5000, regularized=True) == 0
    assert gammainc(-1, 10**30, regularized=True) == 0
    assert gammainc(-1, -5, regularized=True) == 0
    assert gammainc(-1, -5000, regularized=True) == 0
    assert gammainc(-1, -10**30, regularized=True) == 0
    assert gammainc(-1, 3+4j, regularized=True) == 0
    assert gammainc(1, 5, regularized=True).ae(exp(-5))
    assert gammainc(1, 5000, regularized=True).ae(exp(-5000))
    assert gammainc(1, 10**30, regularized=True).ae(exp(-10**30))
    assert gammainc(1, 3+4j, regularized=True).ae(exp(-3-4j))
    assert gammainc(-1000000,2).ae('1.3669297209397347754e-301037', abs_eps=0, rel_eps=8*eps)
    assert gammainc(-1000000,2,regularized=True) == 0
    assert gammainc(-1000000,3+4j).ae('-1.322575609404222361e-698979 - 4.9274570591854533273e-698978j', abs_eps=0, rel_eps=8*eps)
    assert gammainc(-1000000,3+4j,regularized=True) == 0
    assert gammainc(2+3j, 4+5j, regularized=True).ae(0.085422013530993285774-0.052595379150390078503j)
    assert gammainc(1000j, 1000j, regularized=True).ae(0.49702647628921131761 + 0.00297355675013575341j)
    # Generalized
    assert gammainc(3,4,2) == -gammainc(3,2,4)
    assert gammainc(4, 2, 3).ae(1.2593494302978947396)
    assert gammainc(4, 2, 3, regularized=True).ae(0.20989157171631578993)
    assert gammainc(0, 2, 3).ae(0.035852129613864082155)
    assert gammainc(0, 2, 3, regularized=True) == 0
    assert gammainc(-1, 2, 3).ae(0.015219822548487616132)
    assert gammainc(-1, 2, 3, regularized=True) == 0
    assert gammainc(0, 2, 3).ae(0.035852129613864082155)
    assert gammainc(0, 2, 3, regularized=True) == 0
    # Should use upper gammas
    assert gammainc(5, 10000, 12000).ae('1.1359381951461801687e-4327', abs_eps=0, rel_eps=8*eps)
    # Should use lower gammas
    assert gammainc(10000, 2, 3).ae('8.1244514125995785934e4765')
    # GH issue 306
    assert gammainc(3,-1-1j) == 0
    assert gammainc(3,-1+1j) == 0
    assert gammainc(2,-1) == 0
    assert gammainc(2,-1+0j) == 0
    assert gammainc(2+0j,-1) == 0

