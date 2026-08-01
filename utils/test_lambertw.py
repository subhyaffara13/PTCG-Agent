
def test_lambertw():
    k = Symbol('k')

    assert LambertW(x, 0) == LambertW(x)
    assert LambertW(x, 0, evaluate=False) != LambertW(x)
    assert LambertW(0) == 0
    assert LambertW(E) == 1
    assert LambertW(-1/E) == -1
    assert LambertW(-log(2)/2) == -log(2)
    assert LambertW(oo) is oo
    assert LambertW(0, 1) is -oo
    assert LambertW(0, 42) is -oo
    assert LambertW(-pi/2, -1) == -I*pi/2
    assert LambertW(-1/E, -1) == -1
    assert LambertW(-2*exp(-2), -1) == -2
    assert LambertW(2*log(2)) == log(2)
    assert LambertW(-pi/2) == I*pi/2
    assert LambertW(exp(1 + E)) == E

    assert LambertW(x**2).diff(x) == 2*LambertW(x**2)/x/(1 + LambertW(x**2))
    assert LambertW(x, k).diff(x) == LambertW(x, k)/x/(1 + LambertW(x, k))

    assert LambertW(sqrt(2)).evalf(30).epsilon_eq(
        Float("0.701338383413663009202120278965", 30), 1e-29)
    assert re(LambertW(2, -1)).evalf().epsilon_eq(Float("-0.834310366631110"))

    assert LambertW(-1).is_real is False  # issue 5215
    assert LambertW(2, evaluate=False).is_real
    p = Symbol('p', positive=True)
    assert LambertW(p, evaluate=False).is_real
    assert LambertW(p - 1, evaluate=False).is_real is None
    assert LambertW(-p - 2/S.Exp1, evaluate=False).is_real is False
    assert LambertW(S.Half, -1, evaluate=False).is_real is False
    assert LambertW(Rational(-1, 10), -1, evaluate=False).is_real
    assert LambertW(-10, -1, evaluate=False).is_real is False
    assert LambertW(-2, 2, evaluate=False).is_real is False

    assert LambertW(0, evaluate=False).is_algebraic
    na = Symbol('na', nonzero=True, algebraic=True)
    assert LambertW(na).is_algebraic is False
    assert LambertW(p).is_zero is False
    n = Symbol('n', negative=True)
    assert LambertW(n).is_zero is False


def test_lambertw():
    mp.dps = 15
    assert lambertw(0) == 0
    assert lambertw(0+0j) == 0
    assert lambertw(inf) == inf
    assert isnan(lambertw(nan))
    assert lambertw(inf,1).real == inf
    assert lambertw(inf,1).imag.ae(2*pi)
    assert lambertw(-inf,1).real == inf
    assert lambertw(-inf,1).imag.ae(3*pi)
    assert lambertw(0,-1) == -inf
    assert lambertw(0,1) == -inf
    assert lambertw(0,3) == -inf
    assert lambertw(e).ae(1)
    assert lambertw(1).ae(0.567143290409783873)
    assert lambertw(-pi/2).ae(j*pi/2)
    assert lambertw(-log(2)/2).ae(-log(2))
    assert lambertw(0.25).ae(0.203888354702240164)
    assert lambertw(-0.25).ae(-0.357402956181388903)
    assert lambertw(-1./10000,0).ae(-0.000100010001500266719)
    assert lambertw(-0.25,-1).ae(-2.15329236411034965)
    assert lambertw(0.25,-1).ae(-3.00899800997004620-4.07652978899159763j)
    assert lambertw(-0.25,-1).ae(-2.15329236411034965)
    assert lambertw(0.25,1).ae(-3.00899800997004620+4.07652978899159763j)
    assert lambertw(-0.25,1).ae(-3.48973228422959210+7.41405453009603664j)
    assert lambertw(-4).ae(0.67881197132094523+1.91195078174339937j)
    assert lambertw(-4,1).ae(-0.66743107129800988+7.76827456802783084j)
    assert lambertw(-4,-1).ae(0.67881197132094523-1.91195078174339937j)
    assert lambertw(1000).ae(5.24960285240159623)
    assert lambertw(1000,1).ae(4.91492239981054535+5.44652615979447070j)
    assert lambertw(1000,-1).ae(4.91492239981054535-5.44652615979447070j)
    assert lambertw(1000,5).ae(3.5010625305312892+29.9614548941181328j)
    assert lambertw(3+4j).ae(1.281561806123775878+0.533095222020971071j)
    assert lambertw(-0.4+0.4j).ae(-0.10396515323290657+0.61899273315171632j)
    assert lambertw(3+4j,1).ae(-0.11691092896595324+5.61888039871282334j)
    assert lambertw(3+4j,-1).ae(0.25856740686699742-3.85211668616143559j)
    assert lambertw(-0.5,-1).ae(-0.794023632344689368-0.770111750510379110j)
    assert lambertw(-1./10000,1).ae(-11.82350837248724344+6.80546081842002101j)
    assert lambertw(-1./10000,-1).ae(-11.6671145325663544)
    assert lambertw(-1./10000,-2).ae(-11.82350837248724344-6.80546081842002101j)
    assert lambertw(-1./100000,4).ae(-14.9186890769540539+26.1856750178782046j)
    assert lambertw(-1./100000,5).ae(-15.0931437726379218666+32.5525721210262290086j)
    assert lambertw((2+j)/10).ae(0.173704503762911669+0.071781336752835511j)
    assert lambertw((2+j)/10,1).ae(-3.21746028349820063+4.56175438896292539j)
    assert lambertw((2+j)/10,-1).ae(-3.03781405002993088-3.53946629633505737j)
    assert lambertw((2+j)/10,4).ae(-4.6878509692773249+23.8313630697683291j)
    assert lambertw(-(2+j)/10).ae(-0.226933772515757933-0.164986470020154580j)
    assert lambertw(-(2+j)/10,1).ae(-2.43569517046110001+0.76974067544756289j)
    assert lambertw(-(2+j)/10,-1).ae(-3.54858738151989450-6.91627921869943589j)
    assert lambertw(-(2+j)/10,4).ae(-4.5500846928118151+20.6672982215434637j)
    mp.dps = 50
    assert lambertw(pi).ae('1.073658194796149172092178407024821347547745350410314531')
    mp.dps = 15
    # Former bug in generated branch
    assert lambertw(-0.5+0.002j).ae(-0.78917138132659918344 + 0.76743539379990327749j)
    assert lambertw(-0.5-0.002j).ae(-0.78917138132659918344 - 0.76743539379990327749j)
    assert lambertw(-0.448+0.4j).ae(-0.11855133765652382241 + 0.66570534313583423116j)
    assert lambertw(-0.448-0.4j).ae(-0.11855133765652382241 - 0.66570534313583423116j)
    assert lambertw(-0.65475+0.0001j).ae(-0.61053421111385310898+1.0396534993944097723803j)
    # Huge branch index
    w = lambertw(1,10**20)
    assert w.real.ae(-47.889578926290259164)
    assert w.imag.ae(6.2831853071795864769e+20)

