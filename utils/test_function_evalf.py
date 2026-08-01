
def test_function_evalf():
    def eq(a, b, eps):
        return abs(a - b) < eps
    assert eq(sin(1).evalf(15), Float("0.841470984807897"), 1e-13)
    assert eq(
        sin(2).evalf(25), Float("0.9092974268256816953960199", 25), 1e-23)
    assert eq(sin(1 + I).evalf(
        15), Float("1.29845758141598") + Float("0.634963914784736")*I, 1e-13)
    assert eq(exp(1 + I).evalf(15), Float(
        "1.46869393991588") + Float("2.28735528717884239")*I, 1e-13)
    assert eq(exp(-0.5 + 1.5*I).evalf(15), Float(
        "0.0429042815937374") + Float("0.605011292285002")*I, 1e-13)
    assert eq(log(pi + sqrt(2)*I).evalf(
        15), Float("1.23699044022052") + Float("0.422985442737893")*I, 1e-13)
    assert eq(cos(100).evalf(15), Float("0.86231887228768"), 1e-13)

