
def test_evalf_euler_maclaurin():
    assert NS(Sum(1/k**k, (k, 1, oo)), 15) == '1.29128599706266'
    assert NS(Sum(1/k**k, (k, 1, oo)),
              50) == '1.2912859970626635404072825905956005414986193682745'
    assert NS(Sum(1/k - log(1 + 1/k), (k, 1, oo)), 15) == NS(EulerGamma, 15)
    assert NS(Sum(1/k - log(1 + 1/k), (k, 1, oo)), 50) == NS(EulerGamma, 50)
    assert NS(Sum(log(k)/k**2, (k, 1, oo)), 15) == '0.937548254315844'
    assert NS(Sum(log(k)/k**2, (k, 1, oo)),
              50) == '0.93754825431584375370257409456786497789786028861483'
    assert NS(Sum(1/k, (k, 1000000, 2000000)), 15) == '0.693147930560008'
    assert NS(Sum(1/k, (k, 1000000, 2000000)),
              50) == '0.69314793056000780941723211364567656807940638436025'

