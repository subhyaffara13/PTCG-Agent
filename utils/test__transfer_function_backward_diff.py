
def test_TransferFunction_backward_diff():
    # simple transfer function, e.g. ohms law
    tf = TransferFunction(1, a*s+b, s)
    numZ, denZ = backward_diff(tf, T)
    # discretized transfer function with coefs from tf.backward_diff()
    tf_test_backward = TransferFunction(s*numZ[0]+numZ[1], s*denZ[0]+denZ[1], s)
    # corresponding tf with manually calculated coefs
    tf_test_manual = TransferFunction(s * T/(a + b*T), s - a/(a + b*T), s)

    assert S.Zero == (tf_test_backward.simplify()-tf_test_manual.simplify()).simplify().num

