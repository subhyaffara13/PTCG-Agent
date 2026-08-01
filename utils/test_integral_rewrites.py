
def test_integral_rewrites(): #issues 26134, 26144, 26306
    assert expint(n, x).rewrite(Integral).dummy_eq(Integral(t**-n * exp(-t*x), (t, 1, oo)))
    assert Si(x).rewrite(Integral).dummy_eq(Integral(sinc(t), (t, 0, x)))
    assert Ci(x).rewrite(Integral).dummy_eq(log(x) - Integral((1 - cos(t))/t, (t, 0, x)) + EulerGamma)
    assert fresnels(x).rewrite(Integral).dummy_eq(Integral(sin(pi*t**2/2), (t, 0, x)))
    assert fresnelc(x).rewrite(Integral).dummy_eq(Integral(cos(pi*t**2/2), (t, 0, x)))
    assert Ei(x).rewrite(Integral).dummy_eq(Integral(exp(t)/t, (t, -oo, x)))
    assert fresnels(x).diff(x) == fresnels(x).rewrite(Integral).diff(x)
    assert fresnelc(x).diff(x) == fresnelc(x).rewrite(Integral).diff(x)

