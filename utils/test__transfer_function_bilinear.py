
def test_TransferFunction_bilinear():
    # simple transfer function, e.g. ohms law
    tf = TransferFunction(1, a*s+b, s)
    numZ, denZ = bilinear(tf, T)
    # discretized transfer function with coefs from tf.bilinear()
    tf_test_bilinear = TransferFunction(s*numZ[0]+numZ[1], s*denZ[0]+denZ[1], s)
    # corresponding tf with manually calculated coefs
    tf_test_manual = TransferFunction(s * T/(2*(a + b*T/2)) + T/(2*(a + b*T/2)), s + (-a + b*T/2)/(a + b*T/2), s)

    assert S.Zero == (tf_test_bilinear.simplify()-tf_test_manual.simplify()).simplify().num

