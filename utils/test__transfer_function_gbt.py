
def test_TransferFunction_gbt():
    # simple transfer function, e.g. ohms law
    tf = TransferFunction(1, a*s+b, s)
    numZ, denZ = gbt(tf, T, 0.5)
    # discretized transfer function with coefs from tf.gbt()
    tf_test_bilinear = TransferFunction(s * numZ[0] + numZ[1], s * denZ[0] + denZ[1], s)
    # corresponding tf with manually calculated coefs
    tf_test_manual = TransferFunction(s * T/(2*(a + b*T/2)) + T/(2*(a + b*T/2)), s + (-a + b*T/2)/(a + b*T/2), s)

    assert S.Zero == (tf_test_bilinear.simplify()-tf_test_manual.simplify()).simplify().num

    tf = TransferFunction(1, a*s+b, s)
    numZ, denZ = gbt(tf, T, 0)
    # discretized transfer function with coefs from tf.gbt()
    tf_test_forward = TransferFunction(numZ[0], s*denZ[0]+denZ[1], s)
    # corresponding tf with manually calculated coefs
    tf_test_manual = TransferFunction(T/a, s + (-a + b*T)/a, s)

    assert S.Zero == (tf_test_forward.simplify()-tf_test_manual.simplify()).simplify().num

    tf = TransferFunction(1, a*s+b, s)
    numZ, denZ = gbt(tf, T, 1)
    # discretized transfer function with coefs from tf.gbt()
    tf_test_backward = TransferFunction(s*numZ[0], s*denZ[0]+denZ[1], s)
    # corresponding tf with manually calculated coefs
    tf_test_manual = TransferFunction(s * T/(a + b*T), s - a/(a + b*T), s)

    assert S.Zero == (tf_test_backward.simplify()-tf_test_manual.simplify()).simplify().num

    tf = TransferFunction(1, a*s+b, s)
    numZ, denZ = gbt(tf, T, 0.3)
    # discretized transfer function with coefs from tf.gbt()
    tf_test_gbt = TransferFunction(s*numZ[0]+numZ[1], s*denZ[0]+denZ[1], s)
    # corresponding tf with manually calculated coefs
    tf_test_manual = TransferFunction(s*3*T/(10*(a + 3*b*T/10)) + 7*T/(10*(a + 3*b*T/10)), s + (-a + 7*b*T/10)/(a + 3*b*T/10), s)

    assert S.Zero == (tf_test_gbt.simplify()-tf_test_manual.simplify()).simplify().num

