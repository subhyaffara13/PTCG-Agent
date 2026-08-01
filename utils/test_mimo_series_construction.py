
def test_MIMOSeries_construction():
    tf_1 = TransferFunction(a0*s**3 + a1*s**2 - a2*s, b0*p**4 + b1*p**3 - b2*s*p, s)
    tf_2 = TransferFunction(a2*p - s, a2*s + p, s)
    tf_3 = TransferFunction(1, s**2 + 2*zeta*wn*s + wn**2, s)

    tfm_1 = TransferFunctionMatrix([[tf_1, tf_2, tf_3], [-tf_3, -tf_2, tf_1]])
    tfm_2 = TransferFunctionMatrix([[-tf_2], [-tf_2], [-tf_3]])
    tfm_3 = TransferFunctionMatrix([[-tf_3]])
    tfm_4 = TransferFunctionMatrix([[TF3], [TF2], [-TF1]])
    tfm_5 = TransferFunctionMatrix.from_Matrix(Matrix([1/p]), p)

    s8 = MIMOSeries(tfm_2, tfm_1)
    assert s8.args == (tfm_2, tfm_1)
    assert s8.var == s
    assert s8.shape == (s8.num_outputs, s8.num_inputs) == (2, 1)

    s9 = MIMOSeries(tfm_3, tfm_2, tfm_1)
    assert s9.args == (tfm_3, tfm_2, tfm_1)
    assert s9.var == s
    assert s9.shape == (s9.num_outputs, s9.num_inputs) == (2, 1)

    s11 = MIMOSeries(tfm_3, MIMOParallel(-tfm_2, -tfm_4), tfm_1)
    assert s11.args == (tfm_3, MIMOParallel(-tfm_2, -tfm_4), tfm_1)
    assert s11.shape == (s11.num_outputs, s11.num_inputs) == (2, 1)

    # arg cannot be empty tuple.
    raises(ValueError, lambda: MIMOSeries())

    # arg cannot contain SISO as well as MIMO systems.
    raises(TypeError, lambda: MIMOSeries(tfm_1, tf_1))

    # for all the adjacent transfer function matrices:
    # no. of inputs of first TFM must be equal to the no. of outputs of the second TFM.
    raises(ValueError, lambda: MIMOSeries(tfm_1, tfm_2, -tfm_1))

    # all the TFMs must use the same complex variable.
    raises(ValueError, lambda: MIMOSeries(tfm_3, tfm_5))

    # Number or expression not allowed in the arguments.
    raises(TypeError, lambda: MIMOSeries(2, tfm_2, tfm_3))
    raises(TypeError, lambda: MIMOSeries(s**2 + p*s, -tfm_2, tfm_3))
    raises(TypeError, lambda: MIMOSeries(Matrix([1/p]), tfm_3))

