
def test_MIMOFeedback_errors():
    tf1 = TransferFunction(1, s, s)
    tf2 = TransferFunction(s, s**3 - 1, s)
    tf3 = TransferFunction(s, s - 1, s)
    tf4 = TransferFunction(s, s**2 + 1, s)
    tf5 = TransferFunction(1, 1, s)
    tf6 = TransferFunction(-1, s - 1, s)

    tfm_1 = TransferFunctionMatrix([[tf1, tf2], [tf3, tf4]])
    tfm_2 = TransferFunctionMatrix([[tf2, tf3], [tf4, tf1]])
    tfm_3 = TransferFunctionMatrix.from_Matrix(eye(2), var=s)
    tfm_4 = TransferFunctionMatrix([[tf1, tf5], [tf5, tf5]])
    tfm_5 = TransferFunctionMatrix([[-tf3, tf3], [tf3, tf6]])
    # tfm_4 is inverse of tfm_5. Therefore tfm_5*tfm_4 = I
    tfm_6 = TransferFunctionMatrix([[-tf3]])
    tfm_7 = TransferFunctionMatrix([[tf3, tf4]])

    # Unsupported Types
    raises(TypeError, lambda: MIMOFeedback(tf1, tf2))
    raises(TypeError, lambda: MIMOFeedback(MIMOParallel(tfm_1, tfm_2), tfm_3))
    # Shape Errors
    raises(ValueError, lambda: MIMOFeedback(tfm_1, tfm_6, 1))
    raises(ValueError, lambda: MIMOFeedback(tfm_7, tfm_7))
    # sign not 1/-1
    raises(ValueError, lambda: MIMOFeedback(tfm_1, tfm_2, -2))
    # Non-Invertible Systems
    raises(ValueError, lambda: MIMOFeedback(tfm_5, tfm_4, 1))
    raises(ValueError, lambda: MIMOFeedback(tfm_4, -tfm_5))
    raises(ValueError, lambda: MIMOFeedback(tfm_3, tfm_3, 1))
    # Variable not same in both the systems
    tfm_8 = TransferFunctionMatrix.from_Matrix(eye(2), var=p)
    raises(ValueError, lambda: MIMOFeedback(tfm_1, tfm_8, 1))

