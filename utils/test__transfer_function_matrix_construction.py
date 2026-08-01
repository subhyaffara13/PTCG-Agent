
def test_TransferFunctionMatrix_construction():
    tf5 = TransferFunction(a1*s**2 + a2*s - a0, s + a0, s)
    tf4 = TransferFunction(a0*p + p**a1 - s, p, p)

    tfm3_ = TransferFunctionMatrix([[-TF3]])
    assert tfm3_.shape == (tfm3_.num_outputs, tfm3_.num_inputs) == (1, 1)
    assert tfm3_.args == Tuple(Tuple(Tuple(-TF3)))
    assert tfm3_.var == s

    tfm5 = TransferFunctionMatrix([[TF1, -TF2], [TF3, tf5]])
    assert tfm5.shape == (tfm5.num_outputs, tfm5.num_inputs) == (2, 2)
    assert tfm5.args == Tuple(Tuple(Tuple(TF1, -TF2), Tuple(TF3, tf5)))
    assert tfm5.var == s

    tfm7 = TransferFunctionMatrix([[TF1, TF2], [TF3, -tf5], [-tf5, TF2]])
    assert tfm7.shape == (tfm7.num_outputs, tfm7.num_inputs) == (3, 2)
    assert tfm7.args == Tuple(Tuple(Tuple(TF1, TF2), Tuple(TF3, -tf5), Tuple(-tf5, TF2)))
    assert tfm7.var == s

    # all transfer functions will use the same complex variable. tf4 uses 'p'.
    raises(ValueError, lambda: TransferFunctionMatrix([[TF1], [TF2], [tf4]]))
    raises(ValueError, lambda: TransferFunctionMatrix([[TF1, tf4], [TF3, tf5]]))

    # length of all the lists in the TFM should be equal.
    raises(ValueError, lambda: TransferFunctionMatrix([[TF1], [TF3, tf5]]))
    raises(ValueError, lambda: TransferFunctionMatrix([[TF1, TF3], [tf5]]))

    # lists should only support transfer functions in them.
    raises(TypeError, lambda: TransferFunctionMatrix([[TF1, TF2], [TF3, Matrix([1, 2])]]))
    raises(TypeError, lambda: TransferFunctionMatrix([[TF1, Matrix([1, 2])], [TF3, TF2]]))

    # `arg` should strictly be nested list of TransferFunction
    raises(ValueError, lambda: TransferFunctionMatrix([TF1, TF2, tf5]))
    raises(ValueError, lambda: TransferFunctionMatrix([TF1]))

