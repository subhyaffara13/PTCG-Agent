
def test_TransferFunction_forward_diff():
    # simple transfer function, e.g. ohms law
    tf = TransferFunction(1, a*s+b, s)
    numZ, denZ = forward_diff(tf, T)
    # discretized transfer function with coefs from tf.forward_diff()
    tf_test_forward = TransferFunction(numZ[0], s*denZ[0]+denZ[1], s)
    # corresponding tf with manually calculated coefs
    tf_test_manual = TransferFunction(T/a, s + (-a + b*T)/a, s)

    assert S.Zero == (tf_test_forward.simplify()-tf_test_manual.simplify()).simplify().num

