
def test_Feedback_printing():
    tf1 = TransferFunction(p, p + x, p)
    tf2 = TransferFunction(-s + p, p + s, p)
    # Negative Feedback (Default)
    assert latex(Feedback(tf1, tf2)) == \
        r'\frac{\frac{p}{p + x}}{\frac{1}{1} + \left(\frac{p}{p + x}\right) \left(\frac{p - s}{p + s}\right)}'
    assert latex(Feedback(tf1*tf2, TransferFunction(1, 1, p))) == \
        r'\frac{\left(\frac{p}{p + x}\right) \left(\frac{p - s}{p + s}\right)}{\frac{1}{1} + \left(\frac{p}{p + x}\right) \left(\frac{p - s}{p + s}\right)}'
    # Positive Feedback
    assert latex(Feedback(tf1, tf2, 1)) == \
        r'\frac{\frac{p}{p + x}}{\frac{1}{1} - \left(\frac{p}{p + x}\right) \left(\frac{p - s}{p + s}\right)}'
    assert latex(Feedback(tf1*tf2, sign=1)) == \
        r'\frac{\left(\frac{p}{p + x}\right) \left(\frac{p - s}{p + s}\right)}{\frac{1}{1} - \left(\frac{p}{p + x}\right) \left(\frac{p - s}{p + s}\right)}'

