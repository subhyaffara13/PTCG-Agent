
def test_RootSum_evalf():
    rs = RootSum(x**2 + 1, exp)

    assert rs.evalf(n=20, chop=True).epsilon_eq(Float("1.0806046117362794348"))
    assert rs.evalf(n=15, chop=True).epsilon_eq(Float("1.08060461173628"))

    rs = RootSum(x**2 + a, exp, x)

    assert rs.evalf() == rs

